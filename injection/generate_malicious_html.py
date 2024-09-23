import argparse
from pathlib import Path
import jsonlines
import os
import warnings
from inject_malicious_form import inject_form

from tqdm import tqdm

# Remove Huggingface internal warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)

def load_data(path):

    data = []
    with jsonlines.open(path, 'r') as reader:
        for line in reader:
            data.append(line)

    return data

def main():
    parser = argparse.ArgumentParser('Red Team Web Agent')
    parser.add_argument('--attack_type', required=True, choices=["action_grounding", "action_generation", "benign"])
    parser.add_argument('--attack_subtype', choices=["form_type0","form_type1", "form_type2", "copy"])
    parser.add_argument('--attack_position', choices=["most_top", "most_bot", "near_bot_0","near_top_0","near_top_1","near_top_2","near_bot_1","near_bot_2"])
    args = parser.parse_args()

    root_dir = os.getcwd()
    eval_data_path = os.path.join(root_dir, 'data', 'all_instances.jsonl')
    eval_data = load_data(eval_data_path)
    
    attack_type = args.attack_type
    attack_subtype = args.attack_subtype
    attack_position = args.attack_position
      
    progress_bar = tqdm(total=len(eval_data),desc="Processing")

    total = 0
    for item in eval_data:
        progress_bar.update(1)
        
        annotation_id = item["annotation_id"]
        action_id = item["action_id"]
        privacy_type = item["detail_risk_type"]

        if attack_type != "benign":
            ori_html_file_path = os.path.join(root_dir, "data", "webpages_filtered", str(annotation_id), str(action_id),  "modified_file.html")
            
            injected_web_path = inject_form(ori_html_file_path, attack_type, privacy_type, attack_subtype, attack_position)
            if injected_web_path is None:
                print("Injection failed")
                continue
            total += 1
        else:
            print("I am benign")

    print("Total number of examples injected: ", total)

main()