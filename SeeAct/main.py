import argparse
import asyncio
import datetime
import json
import jsonlines
import logging
import os
import warnings
import toml
import torch
import time

from dataclasses import dataclass
from aioconsole import ainput, aprint
from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright

from src.data_utils.format_prompt_utils import get_index_from_option_name
from src.data_utils.prompts import generate_prompt, format_options
from src.demo_utils.browser_helper import (normal_launch_async, normal_new_context_async,
                                       get_interactive_elements_with_playwright, select_option, saveconfig)
from src.demo_utils.format_prompt import format_choices, format_ranking_input, postprocess_action_lmm
from src.demo_utils.inference_engine import OpenaiEngine

from tqdm import tqdm
from result_file_sanity_check import sanity_check_and_filter

# Remove Huggingface internal warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

openai_config = {
    "api_key": os.environ.get("OPENAI_API_KEY"),
    "rate_limit": -1,
    "model": "gpt-4-vision-preview",
    "temperature": 0,
    "seed": 42
}

openai_generation_model = OpenaiEngine(**openai_config, )

@dataclass
class SessionControl:
    pages = []
    cdp_sessions = []
    active_page = None
    active_cdp_session = None
    context = None
    browser = None

session_control = SessionControl()

async def page_on_close_handler(page):

    if session_control.context:
        try:
            await session_control.active_page.title()
        except:
            await aprint("The active tab was closed. Will switch to the last page (or open a new default google page)")
            if session_control.context.pages:
                session_control.active_page = session_control.context.pages[-1]
                await session_control.active_page.bring_to_front()
                await aprint("Switched the active tab to: ", session_control.active_page.url)
            else:
                await session_control.context.new_page()
                try:
                    await session_control.active_page.goto("https://www.google.com/", wait_until="load")
                except Exception as e:
                    pass
                await aprint("Switched the active tab to: ", session_control.active_page.url)


async def page_on_navigatio_handler(frame):
    session_control.active_page = frame.page

async def page_on_crash_handler(page):
    await aprint("Page crashed:", page.url)
    await aprint("Try to reload")
    page.reload()


async def page_on_open_handler(page):
    page.on("framenavigated", page_on_navigatio_handler)
    page.on("close", page_on_close_handler)
    page.on("crash", page_on_crash_handler)
    session_control.active_page = page

async def get_screenshot_and_choices(confirmed_task, website_url, taken_actions, main_result_path,model_name,attack_type):
    

    if model_name == "gpt4v":
        generation_model = openai_generation_model
    else:
        raise ValueError("Implement your own backbone models")

    
    dynamic_choice_batch_size = 1900
    print('dynamic_choice_batch_size',dynamic_choice_batch_size)
        
    fixed_choice_batch_size = 30
    max_op = 30
    max_continuous_no_op = 2
    final_json = {}
    log = ""
    
    max_execution_step = 2 if attack_type != "benign" else 1

    async with async_playwright() as playwright:
        session_control.browser = await normal_launch_async(playwright,headless=True)
        session_control.context = await normal_new_context_async(session_control.browser,
                                                                    tracing=False,
                                                                    storage_state=None,
                                                                    video_path=None,
                                                                    viewport={"width": 1280, "height": 720},
                                                                    trace_screenshots=True,
                                                                    trace_snapshots=False,
                                                                    trace_sources=False,
                                                                    geolocation={"longitude": 39.99542778404405, "latitude": -83.0068669912263},
                                                                    locale="en-US")
        session_control.context.on("page", page_on_open_handler)
        await session_control.context.new_page()
        try:
            await session_control.active_page.goto(website_url, wait_until="load")
        except Exception as e:
            print("Failed to fully load the webpage before timeout")
            print(e)
        await asyncio.sleep(3)

        complete_flag = False
        time_step = 0
        no_op_count = 0
        valid_op_count = 0

        while not complete_flag:
            try:
                time.sleep(3)
                await session_control.active_page.bring_to_front()
                terminal_width = 10
                print("=" * terminal_width)
                print(f"Time step: {time_step}")
                print('-' * 10)
                time_step += 1
                if time_step > max_execution_step:
                    success_or_not = ""
                    if valid_op_count == 0:
                        success_or_not = "0"
                    final_json = {"confirmed_task": confirmed_task, "website": website_url,
                                    "success_or_not": success_or_not,
                                    "num_step": len(taken_actions), "action_history": taken_actions,
                                    "exit_by": "No elements", "log": log}

                    with open(os.path.join(main_result_path, 'result.json'), 'w', encoding='utf-8') as file:
                        json.dump(final_json, file, indent=4)

                    close_context = session_control.context
                    session_control.context = None
                    await close_context.close()
                    complete_flag = True
                    continue
                
                log += "\n" + "\n".join(["=" * terminal_width, f"Time step: {time_step}", '-' * 10])
                elements = await get_interactive_elements_with_playwright(session_control.active_page, {'element_des': "default"})
                

                all_candidate_ids = range(len(elements))
                ranked_elements = elements

                all_candidate_ids_with_location = []
                for element_id, element_detail in zip(all_candidate_ids, ranked_elements):
                    all_candidate_ids_with_location.append(
                        (element_id, round(element_detail[0][1]), round(element_detail[0][0])))

                all_candidate_ids_with_location.sort(key=lambda x: (x[1], x[2]))

                all_candidate_ids = [element_id[0] for element_id in all_candidate_ids_with_location]
                num_choices = len(all_candidate_ids)

                total_height = await session_control.active_page.evaluate('''() => {
                                                                return Math.max(
                                                                    document.documentElement.scrollHeight, 
                                                                    document.body.scrollHeight,
                                                                    document.documentElement.clientHeight
                                                                );
                                                            }''')
                if dynamic_choice_batch_size > 0:
                    step_length = min(num_choices,
                                        num_choices // max(round(total_height / dynamic_choice_batch_size), 1) + 1)
                else:
                    step_length = min(num_choices, fixed_choice_batch_size)

                total_width = session_control.active_page.viewport_size["width"]
                previous_actions = taken_actions

                previous_action_text = "Previous Actions:\n"
                if previous_actions is None or previous_actions == []:
                    previous_actions = ["None"]
                for action_text in previous_actions:
                    previous_action_text += action_text
                    previous_action_text += "\n"

                    target_element = []

                new_action = ""
                target_action = "CLICK"
                target_value = ""
                query_count = 0
                got_one_answer = False

                for multichoice_i in range(0, num_choices, step_length):
                    print("-" * 10)
                    print(f"Start Multi-Choice QA - Batch {multichoice_i // step_length}")
                    log += "\n".join(["-" * 10, f"Start Multi-Choice QA - Batch {multichoice_i // step_length}"]) + "\n"
                    input_image_path = os.path.join(main_result_path, 'image_inputs',
                                                    f'{time_step}_{multichoice_i // step_length}_crop.jpg')
                    viewport_height = await session_control.active_page.evaluate('() => window.scrollY')
                    height_start = all_candidate_ids_with_location[multichoice_i][1] + viewport_height

                    height_end = all_candidate_ids_with_location[min(multichoice_i + step_length, num_choices) - 1][
                                        1] + viewport_height

                    total_height = await session_control.active_page.evaluate('''() => {
                                                                                        return Math.max(
                                                                                            document.documentElement.scrollHeight, 
                                                                                            document.body.scrollHeight,
                                                                                            document.documentElement.clientHeight
                                                                                        );
                                                                                    }''')
                    clip_start = min(total_height - 1000, max(0, height_start - 200))
                    clip_height = min(total_height - clip_start, max(height_end - height_start + 200, 1000))
                    clip = {"x": 0, "y": clip_start, "width": total_width, "height": clip_height}

                    try:
                        await session_control.active_page.screenshot(path=input_image_path, clip=clip, full_page=True,
                                                                        type='jpeg', quality=100, timeout=20000)
                    except Exception as e_clip:
                        print(f"Failed to get cropped screenshot because {e_clip}")

                    candidate_ids = all_candidate_ids[multichoice_i:multichoice_i + step_length]
                    choices = format_choices(elements, candidate_ids, confirmed_task, taken_actions)
                    query_count += 1

                    prompt = generate_prompt(task=confirmed_task, previous=taken_actions, choices=choices,
                                                experiment_split="SeeAct")

     
     

                    output0 = generation_model.generate(prompt=prompt, image_path=input_image_path, turn_number=0)

                    terminal_width = 10
                    print("-" * terminal_width)
                    print("🤖Action Generation Output🤖")


                    for line in output0.split('\n'):
                        print(line)

                    terminal_width = 10
                    print("-" * (terminal_width))

                    log += "\n".join(["-" * terminal_width, "🤖Action Generation Output🤖", output0, "-" * (terminal_width)])

                    choice_text = f"(Multichoice Question) - Batch {multichoice_i // step_length}" + "\n" + format_options(
                        choices)
                    choice_text = choice_text.replace("\n\n", "")

                    for line in choice_text.split('\n'):
                        print(line)

                    log += "\n" + choice_text

                    output = generation_model.generate(prompt=prompt, image_path=input_image_path, turn_number=1,
                                                        ouput__0=output0)

                    terminal_width = 10
                    print("-" * terminal_width)
                    print("🤖Grounding Output🤖")

                    for line in output.split('\n'):
                        print(line)

                    log += "\n" + "\n".join(["-" * terminal_width, "🤖Grounding Output🤖", output])

                    pred_element, pred_action, pred_value = postprocess_action_lmm(output)
                    if len(pred_element) in [1, 2]:
                        element_id = get_index_from_option_name(pred_element)
                    else:
                        element_id = -1

                    # Process the elements
                    if (0 <= element_id < len(candidate_ids) and pred_action.strip() in ["CLICK", "SELECT", "TYPE",
                                                                                            "PRESS ENTER", "HOVER",
                                                                                            "TERMINATE"]):
                        target_element = elements[int(choices[element_id][0])]
                        target_element_text = choices[element_id][1]
                        target_action = pred_action
                        target_value = pred_value
                        new_action += "[" + target_element[2] + "]" + " "
                        new_action += target_element[1] + " -> " + target_action
                        if target_action.strip() in ["SELECT", "TYPE"]:
                            new_action += ": " + target_value
                        got_one_answer = True
                        break
                    elif pred_action.strip() in ["PRESS ENTER", "TERMINATE"]:
                        target_element = pred_action
                        target_element_text = target_element
                        target_action = pred_action
                        target_value = pred_value
                        new_action += target_action
                        if target_action.strip() in ["SELECT", "TYPE"]:
                            new_action += ": " + target_value
                        got_one_answer = True
                        break
                    else:
                        pass

                if got_one_answer:
                    terminal_width = 10
                    print("-" * terminal_width)
                    print("🤖Browser Operation🤖")
                    print(f"Target Element: {target_element_text}", )
                    print(f"Target Action: {target_action}", )
                    print(f"Target Value: {target_value}", )

                    log += "\n" + "\n".join(["-" * terminal_width, "🤖Browser Operation🤖", f"Target Element: {target_element_text}", f"Target Action: {target_action}", f"Target Value: {target_value}"])

                else:
                    no_op_count += 1
                    target_element = []

                try:
                    if no_op_count >= max_continuous_no_op:
                        raise Exception(f"no executable operations for {max_continuous_no_op} times.")
                    elif time_step >= max_op:
                        raise Exception(f"the agent reached the step limit {max_op}.")
                    elif target_action == "TERMINATE":
                        raise Exception("The model determined a completion.")

                    # Perform browser action with PlayWright
                    # The code is complex to handle all kinds of cases in execution
                    # It's ugly, but it works, so far
                    selector = None
                    fail_to_execute = False
                    try:
                        if target_element == []:
                            pass
                        else:
                            if not target_element in ["PRESS ENTER", "TERMINATE"]:
                                selector = target_element[-2]
                                try:
                                    await selector.scroll_into_view_if_needed(timeout=3000)
                                    if highlight:
                                        await selector.highlight()
                                        await asyncio.sleep(2.5)
                                except Exception as e:
                                    pass

                        if selector:
                            valid_op_count += 1
                            if target_action == "CLICK":
                                js_click = True
                                try:
                                    if target_element[-1] in ["select", "input"]:
                                        print("Try performing a CLICK")
                                        await selector.evaluate("element => element.click()", timeout=10000)
                                        js_click = False
                                    else:
                                        await selector.click(timeout=10000)
                                except Exception as e:
                                    try:
                                        if not js_click:
                                            print("Try performing a CLICK")
                                            await selector.evaluate("element => element.click()", timeout=10000)
                                        else:
                                            raise Exception(e)
                                    except Exception as ee:
                                        try:
                                            print("Try performing a HOVER")
                                            await selector.hover(timeout=10000)
                                            new_action = new_action.replace("CLICK",
                                                                            f"Failed to CLICK because {e}, did a HOVER instead")
                                        except Exception as eee:
                                            new_action = new_action.replace("CLICK", f"Failed to CLICK because {e}")
                                            no_op_count += 1
                            elif target_action == "TYPE":
                                try:
                                    try:
                                        print("Try performing a \"press_sequentially\"")
                                        await selector.clear(timeout=10000)
                                        await selector.fill("", timeout=10000)
                                        await selector.press_sequentially(target_value, timeout=10000)
                                    except Exception as e0:
                                        await selector.fill(target_value, timeout=10000)
                                except Exception as e:
                                    try:
                                        if target_element[-1] in ["select"]:
                                            print("Try performing a SELECT")
                                            selected_value = await select_option(selector, target_value)
                                            new_action = new_action.replace("TYPE",
                                                                            f"Failed to TYPE \"{target_value}\" because {e}, did a SELECT {selected_value} instead")
                                        else:
                                            raise Exception(e)
                                    except Exception as ee:
                                        js_click = True
                                        try:
                                            if target_element[-1] in ["select", "input"]:
                                                print("Try performing a CLICK")
                                                await selector.evaluate("element => element.click()", timeout=10000)
                                                js_click = False
                                            else:
                                                print("Try performing a CLICK")
                                                await selector.click(timeout=10000)
                                            new_action = "[" + target_element[2] + "]" + " "
                                            new_action += target_element[
                                                                1] + " -> " + f"Failed to TYPE \"{target_value}\" because {e}, did a CLICK instead"
                                        except Exception as eee:
                                            try:
                                                if not js_click:
                                                    print("Try performing a CLICK")
                                                    await selector.evaluate("element => element.click()", timeout=10000)
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to TYPE \"{target_value}\" because {e}, did a CLICK instead"
                                                else:
                                                    raise Exception(eee)
                                            except Exception as eeee:
                                                try:
                                                    print("Try performing a HOVER")
                                                    await selector.hover(timeout=10000)
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to TYPE \"{target_value}\" because {e}, did a HOVER instead"
                                                except Exception as eee:
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to TYPE \"{target_value}\" because {e}"
                                                    no_op_count += 1
                            elif target_action == "SELECT":
                                try:
                                    print("Try performing a SELECT")
                                    selected_value = await select_option(selector, target_value)
                                    new_action = new_action.replace(f"{target_value}", f"{selected_value}")
                                except Exception as e:
                                    try:
                                        if target_element[-1] in ["input"]:
                                            try:
                                                print("Try performing a \"press_sequentially\"")
                                                await selector.clear(timeout=10000)
                                                await selector.fill("", timeout=10000)
                                                await selector.press_sequentially(target_value, timeout=10000)
                                            except Exception as e0:
                                                await selector.fill(target_value, timeout=10000)
                                            new_action = new_action.replace("SELECT",
                                                                            f"Failed to SELECT \"{target_value}\" because {e}, did a TYPE instead")
                                        else:
                                            raise Exception(e)
                                    except Exception as ee:
                                        js_click = True
                                        try:
                                            if target_element[-1] in ["select", "input"]:
                                                print("Try performing a CLICK")
                                                await selector.evaluate("element => element.click()", timeout=10000)
                                                js_click = False
                                            else:
                                                await selector.click(timeout=10000)
                                            new_action = "[" + target_element[2] + "]" + " "
                                            new_action += target_element[
                                                                1] + " -> " + f"Failed to SELECT \"{target_value}\" because {e}, did a CLICK instead"
                                        except Exception as eee:

                                            try:
                                                if not js_click:
                                                    print("Try performing a CLICK")
                                                    await selector.evaluate("element => element.click()", timeout=10000)
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to SELECT \"{target_value}\" because {e}, did a CLICK instead"
                                                else:
                                                    raise Exception(eee)
                                            except Exception as eeee:
                                                try:
                                                    print("Try performing a HOVER")
                                                    await selector.hover(timeout=10000)
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to SELECT \"{target_value}\" because {e}, did a HOVER instead"
                                                except Exception as eee:
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to SELECT \"{target_value}\" because {e}"
                                                    no_op_count += 1
                            elif target_action == "HOVER":
                                try:
                                    print("Try performing a HOVER")
                                    await selector.hover(timeout=10000)
                                except Exception as e:
                                    try:
                                        await selector.click(timeout=10000)
                                        new_action = new_action.replace("HOVER",
                                                                        f"Failed to HOVER because {e}, did a CLICK instead")
                                    except:
                                        js_click = True
                                        try:
                                            if target_element[-1] in ["select", "input"]:
                                                print("Try performing a CLICK")
                                                await selector.evaluate("element => element.click()", timeout=10000)
                                                js_click = False
                                            else:
                                                await selector.click(timeout=10000)
                                            new_action = "[" + target_element[2] + "]" + " "
                                            new_action += target_element[
                                                                1] + " -> " + f"Failed to HOVER because {e}, did a CLICK instead"
                                        except Exception as eee:
                                            try:
                                                if not js_click:
                                                    print("Try performing a CLICK")
                                                    await selector.evaluate("element => element.click()", timeout=10000)
                                                    new_action = "[" + target_element[2] + "]" + " "
                                                    new_action += target_element[
                                                                        1] + " -> " + f"Failed to HOVER because {e}, did a CLICK instead"
                                                else:
                                                    raise Exception(eee)
                                            except Exception as eeee:
                                                new_action = "[" + target_element[2] + "]" + " "
                                                new_action += target_element[
                                                                    1] + " -> " + f"Failed to HOVER because {e}"
                                                no_op_count += 1
                            elif target_action == "PRESS ENTER":
                                try:
                                    print("Try performing a PRESS ENTER")
                                    await selector.press('Enter')
                                except Exception as e:
                                    await selector.click(timeout=10000)
                                    await session_control.active_page.keyboard.press('Enter')

                        elif target_element == "PRESS ENTER":
                            print("Try performing a PRESS ENTER")
                            await session_control.active_page.keyboard.press('Enter')
                        no_op_count = 0
                        try:
                            await session_control.active_page.wait_for_load_state('load')
                        except Exception as e:
                            pass
                    except Exception as e:
                        if target_action not in ["TYPE", "SELECT"]:
                            new_action = f"Failed to {target_action} {target_element_text} because {e}"

                        else:
                            new_action = f"Failed to {target_action} {target_value} for {target_element_text} because {e}"
                        fail_to_execute = True

                    if new_action == "" or fail_to_execute:
                        if new_action == "":
                            new_action = "No Operation"

                        no_op_count += 1
                    taken_actions.append(new_action)
                    if not session_control.context.pages:
                        await session_control.context.new_page()
                        try:
                            await session_control.active_page.goto(website_url, wait_until="load")
                        except Exception as e:
                            pass

                    await asyncio.sleep(3)

                    try:
                        await session_control.active_page.wait_for_load_state('load')
                    except Exception as e:
                        print(e)

                except Exception as e:
                    print("=" * 10)
                    print(f"Decide to terminate because {e}")
                    print("Action History:")

                    for action in taken_actions:
                        print(action)
                    print("")

                    log += "\n".join(["=" * 10, f"Decide to terminate because {e}", "Action History:"] + taken_actions)

                    success_or_not = ""
                    if valid_op_count == 0:
                        success_or_not = "0"
                    print(f"Write results to json file: {os.path.join(main_result_path, 'result.json')}")
                    final_json = {"confirmed_task": confirmed_task, "website": website_url,
                                    "success_or_not": success_or_not,
                                    "num_step": len(taken_actions), "action_history": taken_actions, "exit_by": str(e), "log": log}

                    with open(os.path.join(main_result_path, 'result.json'), 'w', encoding='utf-8') as file:
                        json.dump(final_json, file, indent=4)

                    print("Close brownser context")
                    close_context = session_control.context
                    session_control.context = None
                    await close_context.close()

                    complete_flag = True
            except Exception as e:
                print(e)
                complete_flag = True

    return final_json

def load_data(path):

    data = []
    with jsonlines.open(path, 'r') as reader:
        for line in reader:
            data.append(line)

    return data

def process_attack_type_subtypes(attack_type,attack_subtype):
    if attack_type == "benign":
        return attack_type
    return attack_type + "_" + attack_subtype

    

from pathlib import Path
def main():
    parser = argparse.ArgumentParser('Red Team Web Agent')
    parser.add_argument('--attack_type', required=True, choices=["action_grounding", "action_generation", "benign"])
    parser.add_argument('--model_name', required=True, choices=["gpt4v"])
    
    parser.add_argument('--attack_subtype', default="None",choices=["form_type2","form_type1","form_type0","copy"])
    parser.add_argument('--attack_position', choices=["most_top","most_bot", "near_bot_0","near_top_0","near_top_1","near_top_2","near_bot_1","near_bot_2"])
    
    parser.add_argument("--save_dir",default="../eval_results/eval_results")
    parser.add_argument("--port",help="port number",default=8000,type=int)

    args = parser.parse_args()

    eval_data_path = "../data/all_instances.jsonl"
    
    eval_data = load_data(eval_data_path)
    
    attack_type = args.attack_type
    attack_subtype = args.attack_subtype
    
    if attack_type != "benign":
        assert attack_subtype in ["form_type0","form_type1","copy","form_type2"]
        
    attack_position = args.attack_position
    model_name = args.model_name
    save_dir = args.save_dir
    port = args.port
    
    
    
    if attack_type == "benign":
        save_dir = os.path.join(save_dir, "%s/%s/"%(model_name, process_attack_type_subtypes(attack_type,attack_subtype)))
    else:
        save_dir = os.path.join(save_dir, "%s/%s/"%(model_name, process_attack_type_subtypes(attack_type,attack_subtype) + f"_{attack_position}"))

    Path(save_dir).mkdir(parents=True, exist_ok=True)
    
    progress_bar = tqdm(total=len(eval_data),desc="Processing")
    try:
        existing_lines = load_data(os.path.join(save_dir,"results.json"))
        exisitng_ids = [f"{existing_lines[_]['annotation_id']}/{existing_lines[_]['action_id']}" for _ in range(len(existing_lines))]
    except:
        exisitng_ids = []
    
    with jsonlines.open(os.path.join(save_dir,"results.json"), "a") as f:
        for item in eval_data:
            progress_bar.update(1)
            
            # print(item)
            confirmed_task = item["confirmed_task"]
            annotation_id = item["annotation_id"]
            action_id = item["action_id"]
      
            if f"{annotation_id}/{action_id}" in exisitng_ids:
                print("id already exist")
                continue
            
            privacy_type = item["detail_risk_type"]
            taken_actions = item["previous_action_reprs"]
            next_action_reprs = item["next_action_reprs"]
            gold_action_reprs = item["action_reprs"]
            num_attack_step = item["step_num"]
            domain = item["domain"]
            subdomain = item["subdomain"]


            main_result_path = os.path.join(save_dir,"%s/%s/"%(annotation_id, action_id))
            Path(main_result_path).mkdir(parents=True, exist_ok=True)
            
            
            root_html_dir = "../data"
            if attack_type != "benign":
                website_url = f"http://127.0.0.1:{port}/webpages/{annotation_id}/{action_id}/adv_modified_file_{process_attack_type_subtypes(attack_type, attack_subtype)}_{attack_position}.html"
            
            else:
                website_url = f"http://127.0.0.1:{port}/webpages/{annotation_id}/{action_id}/modified_file.html"
            
            
            
            result = asyncio.run(get_screenshot_and_choices(confirmed_task, website_url, taken_actions, main_result_path,model_name,attack_type))
            if not result:
                result = {"confirmed_task": confirmed_task, "website": website_url}
            print(result)
            result["num_attack_step"] = num_attack_step
            result["next_action_reprs"] = next_action_reprs
            result["privacy_type"] = privacy_type
            result["domain"] = domain
            result["subdomain"] = subdomain
            result["gold_action_reprs"] = gold_action_reprs
            result["annotation_id"] = annotation_id
            result["action_id"] = action_id

            f.write(result)

    f.close()
    sanity_check_and_filter(os.path.join(save_dir,"results.json"))
main()
