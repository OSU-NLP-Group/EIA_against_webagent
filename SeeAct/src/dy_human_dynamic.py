import asyncio
import pdb
import re
import time
import uuid
import os
import json
from collections import defaultdict
import pyperclip
from dataclasses import dataclass
import random
import torch

import openai
from utils.browser_helper import (
    normal_launch_async,
    normal_new_context_async,
)
from utils.format_prompt import original_prompt, format_llm_input
from utils.format_prompt import postprocess_action_llm
from utils.format_prompt import format_ranking_input
from utils.llm_engines import OpenaiEngine
from utils.dom_utils import get_tree_repr, prune_tree
from utils.ranking_model import CrossEncoder
import numpy as np

from InquirerPy import inquirer
from playwright.async_api import async_playwright

import lxml

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)


import logging, datetime



sys_prompt = "Imagine that you are imitating human doing web navigation for a task step by step. At each stage, " \
             "you can see the webpage like human by a given screenshot, and know the previous action history indicating what have done before the current stage. " \
             "You can click an element with the mouse, select an option, or type some text with the keyboard.\n\nYou " \
             "are asked to complete the following task: "


question_description_new_human_eval = "Below the screenshot is the webpage you see. Follow the following guidance to think step by step before clearly outlining the next action step at current stage that user would like to take(Not all the subsequent actions):\n\n(Current Webpage Identification)Firstly, think about what the current webpage is.\n\n(Previous Action Analysis)Secondly, combining with the screenshot, analyze each step of the previous action history and the intention of each of them one by one. Particularly, pay more attention to the last step, which may be more related to what you should do now as the next step.\n\n(Screenshot Details Analysis) Closely examine the screenshot to check the status of every part of the webpage, to understand what you can operate with, and what have been set or completed. You should closely examine the details of the screenshot to see what steps has been completed by previous actions even though you are given the textual previous actions. Because some effect of previous actions may not be clearly and sufficiently recorded by the textual history, you should really closely evaluate the status of every part of the webpage to understand what have done.\n\n(Intended Action Based on Webpage and Analysis)Then, based on your analysis, in conjunction with human's web browsing habits and the logic of web design, conclude which element in the webpage will users operate with as the first next target element, where the element is located, and what the corresponding operation is. Please clearly specify which element to operate with. Closely examine the screenshot to provide its detailed location, description, textual content(if it has) and so on to help identify your answer. If there are multiple elements that are similar to your target element, use more precise description to make sure people can distinguish your target element from them through your answer."



def generate_query_prompt(system_prompt=sys_prompt, task="", previous_actions=None, question_description=question_description_new_human_eval):
    """
    Generate the first phase prompt to ask model to generate general descriptions about {environment, high-level plans, next step action}
    Each experiment will have a similar prompt in this phase
    This prompt is used to generate models' thoughts without disrupt of formatting/referring prompts
    """
    query_text = ""

    # System Prompt
    query_text += system_prompt

    # Task Description
    query_text += task
    query_text += "\n\n"

    # Previous Actions
    previous_action_text = "Previous Actions:\n"
    if previous_actions is None:
        previous_actions = []
    for action_text in previous_actions:
        previous_action_text += action_text
        previous_action_text += "\n"
    query_text += previous_action_text
    query_text += "\n"

    # Question Description
    query_text += question_description
    return query_text

def custom_print(message, logger):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')
    logger.debug(message)
    print(f"[{formatted_time}] {message}")




interactive_element_roles = {
    "button",
    "checkbox",
    "radio",
    "combobox",
    "textbox",
    "listbox",
    "menu",
    "tree",
    "a",
}


async def scroll_element_into_full_view(page, element):
    extra_padding = 100  # 额外的像素距离
    rect = await element.evaluate('''element => {
        const rect = element.getBoundingClientRect();
        return {
            top: rect.top,
            bottom: rect.bottom,
            height: rect.height,
            viewportHeight: window.innerHeight
        };
    }''')

    # 判断元素是否完全可见
    if rect["top"] < 0 or rect["bottom"] > rect["viewportHeight"]:
        # 计算居中的滚动位置
        new_scroll_y = rect["top"] - (rect["viewportHeight"] - rect["height"]) / 2 - extra_padding
        await page.evaluate(f'window.scrollTo(0, window.scrollY + {new_scroll_y})')



from difflib import SequenceMatcher


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()




@dataclass
class SessionControl:
    pages = []
    cdp_sessions = []
    active_page = None
    active_cdp_session = None
    context = None
    browser = None


session_control = SessionControl()


async def init_cdp_session(page):
    cdp_session = await page.context.new_cdp_session(page)
    await cdp_session.send("DOM.enable")
    await cdp_session.send("Overlay.enable")
    await cdp_session.send("Accessibility.enable")
    await cdp_session.send("Page.enable")
    await cdp_session.send("Emulation.setFocusEmulationEnabled", {"enabled": True})
    return cdp_session


async def page_on_close_handler(page):
    for idx, p in enumerate(session_control.pages):
        if p == page:
            break
    session_control.pages.pop(idx)
    cdp_session = session_control.cdp_sessions.pop(idx)


async def page_on_open_handler(page):
    page.on("close", page_on_close_handler)
    session_control.pages.append(page)
    session_control.active_page = page
    cdp_session = await init_cdp_session(page)
    session_control.active_cdp_session = cdp_session
    session_control.cdp_sessions.append(cdp_session)


import readline


async def main() -> None:
    is_demo = False
    from task_and_website import tasks_from_website, tasks_from_domain, tasks_from_task, website_dict

    test_split = "final_merged"
    with open(f'dynamic_{test_split}.json', 'r') as file:
        query_tasks = json.load(file)
    for one_query_task in query_tasks:
        annotated_id = one_query_task["annotation_id"]
        main_result_path = f"dynamic_results_exp4/Online_Results/oracle/{annotated_id}"
        if not os.path.exists(main_result_path):
            os.makedirs(main_result_path)
            # print(annotated_id)
            # continue
        else:
            print("Already Existed")
            continue


        confirmed_task = one_query_task["confirmed_task"]
        confirmed_website = one_query_wtask["website"]
        confirmed_website_url = website_dict[confirmed_website]


        logger = logging.getLogger(f"{annotated_id}")
        logger.setLevel(logging.DEBUG)
        log_fh = logging.FileHandler(f'{main_result_path}/{annotated_id}.log')
        log_fh.setLevel(logging.DEBUG)
        log_format = logging.Formatter('%(asctime)s - %(message)s')
        log_fh.setFormatter(log_format)
        logger.addHandler(log_fh)
        custom_print(f"Id: {annotated_id}", logger)
        custom_print(f"Website: {confirmed_website_url}", logger)
        custom_print(f"Task: {confirmed_task}", logger)
        no_ad=False
        async with async_playwright() as playwright:

            custom_print("Start to launch playwright", logger)
            session_control.browser = await normal_launch_async(playwright)
            custom_print("Playwright launched", logger)

            # Setup context however you like.
            session_control.context = await normal_new_context_async(

                session_control.browser,
                # storage_state="/Users/gemini/Downloads/storage_base.json",
                tracing=True,
                # video_path=main_result_path if do_video_recording else "None",
                viewport={"width": 1344, "height": 1035},
            # record_video_size={"width": 1344, "height": 840} if do_video_recording else "None"
            )

            await session_control.context.tracing.start_chunk()

            session_control.context.on("page", page_on_open_handler)

            custom_print("context launched", logger)

            # Pause the page, and start recording manually.
            await session_control.context.new_page()
            if is_demo:
                website_url = await inquirer.text(
                    message="Please enter URL link to the website you want to visit").execute_async()
                if website_url == "":
                    website_url = confirmed_website_url
                selected_website = [website_url]
            else:
                selected_website = [confirmed_website_url]
                try:
                    await session_control.active_page.goto(selected_website[0], wait_until="load")
                except Exception as e:
                    print(e)
                    pass


            if is_demo:
                objective = await inquirer.text(
                    message="Please enter the objective you want the agent to perform").execute_async()
                if objective == "":
                    objective = confirmed_task
            else:
                objective = confirmed_task


            taken_actions = []
            current_action_ids = set()
            complete_flag = False

            time_step = 0

            no_op_count = 0
            valid_op_count = 0

            start_y=0
            while not complete_flag:
                try:
                    custom_print("------------------------", logger)
                    custom_print(f"Time step: {time_step}", logger)
                    time_step += 1

                    # await asyncio.sleep(10)
                    image_save_path=f'{main_result_path}/image_inputs/{time_step}.png'

                    if not os.path.exists(main_result_path):
                        os.makedirs(main_result_path)

                    # if not no_ad:
                    #     # await asyncio.sleep(10)
                    #     print("Please wait until ensuring no ads and login")
                    #     webpage_status = input()
                    #     if webpage_status == "no":
                    #         no_ad = True
                    #     if webpage_status == "login":
                    #         raise Exception("Force logging in, please delete this task.")
                    #
                    # else:
                    #     pass



                    # viewport_width = session_control.active_page.viewport_size['width']
                    # viewport_height = session_control.active_page.viewport_size['height']

                    # 获取当前视窗的滚动位置
                    # scroll_x, scroll_y = await session_control.active_page.evaluate("() => [window.scrollX, window.scrollY]")
                    #

                    # total_height =await  session_control.active_page.evaluate("() => document.body.scrollHeight")

                    # screenshot_height = total_height - start_y

                    # clip = {'x': 0, 'y': start_y, 'width': viewport_width, 'height': min(screenshot_height,2500)}
                    # session_control.active_page.screenshot(path="screenshot.png",)
                    # print("scroll_y:",scroll_y)
                    # print("screenshot_height",screenshot_height)
                    # print("CPIP:",clip)



                    # await session_control.active_page.screenshot(path=image_save_path, clip=clip,)


                    get_prompts = generate_query_prompt(task=confirmed_task,previous_actions=taken_actions)
                    get_prompts+="""\n\n(Summarization) Summarize your answer of first next target element and action into 
ELEMENT: (If the web page element you want to operate with has text content or an icon exactly inside the element, please also include the exact text content or description of the icon.)
ACTION:
VALUE:

(Record History) Finally, summarize your summarization into one sentence to record this action step as history."""
                    custom_print(f"Query-GPT-4V-Step: {time_step}",logger)

                    print(f"Here's the prompts. It has been copied. Please manually query GPT4V")

                    custom_print(f"####### Prompts at step:{time_step} ##########", logger)
                    custom_print(get_prompts,logger)
                    custom_print(f"####### Output at step:{time_step} ##########",logger)

                    gpt4v_output=""

                    print("Please input the output")

                    while True:
                        line = input()
                        if line != "dd":
                            gpt4v_output+= (line+"\n")
                        else:
                            break

                    print(gpt4v_output)


                    custom_print(gpt4v_output,logger)

                    print("Please input the generated action as history here. Notice do not contain a \"\\n\"")

                    new_action = f"{time_step}. "+input()
                    if new_action==f"{time_step}. ":
                        new_action+="No operation."
                        no_op_count += 1
                    else:
                        no_op_count = 0
                    if new_action==f"{time_step}. 0":
                        taken_actions.append("Manually Exit")
                        raise Exception("Manually Exit")
                    if new_action == f"{time_step}. 1":
                        # taken_actions.append("Manually Exit")
                        new_action = f"{time_step}. scroll down"
                        # start_y+=2500
                        # await session_control.active_page.evaluate("window.scrollBy(0, 2500)")
                    # else:
                    #     start_y=0
                    valid_op_count+=1

                    if no_op_count >= 2:
                        raise Exception("No choices for twice. Raise an exception and exit")
                    if time_step >= 40:
                        raise Exception("Reached time step limit. Raise an exception and exit")
                    taken_actions.append(new_action)
                    custom_print("New Action History:", logger)
                    for i_action in taken_actions:
                        custom_print(i_action, logger)

                    print("Should we stop now?")
                    webpage_status = input()
                    if webpage_status == "1":
                        raise Exception("Manually exit.")

                    try:
                        session_control.active_page.wait_for_load_state('load')
                    except:
                        pass



                except Exception as e:
                    custom_print(e, logger)
                    custom_print("-----------------------", logger)
                    custom_print("Decide to terminate", logger)


                    custom_print("Save playwright trace file ", logger)
                    await session_control.context.tracing.stop_chunk(path=f"{main_result_path}/playwright_traces.zip")
                    custom_print("Close brownser context", logger)
                    await session_control.context.close()


                    custom_print("Write result json file", logger)
                    print("Please indicate if it is a success, by \"0\" or \"1\"", logger)
                    success_or_not = input()
                    print("Do you have specific notes for this task?", logger)
                    additional_notes = input()

                    final_json = {"confirmed_task": confirmed_task, "website": confirmed_website,
                                  "annotation_id": annotated_id, "success_or_not": success_or_not,
                                  "step length": len(taken_actions), "action series": taken_actions,
                                  "additional_notes": additional_notes if additional_notes else "", "exit_by": str(e)}

                    with open(f"{main_result_path}/result.json", 'w') as file:
                        json.dump(final_json, file, indent=4)

                    custom_print("-----------------------", logger)
                    custom_print("Action History:", logger)

                    for i_action in taken_actions:
                        custom_print(i_action, logger)
                    custom_print("-----------------------", logger)

                    complete_flag = True


if __name__ == "__main__":
    asyncio.run(main())
