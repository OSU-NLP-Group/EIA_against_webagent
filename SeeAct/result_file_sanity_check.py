import jsonlines
import argparse

def sanity_check_and_filter(file):

    print(file)
    with jsonlines.open(file= file) as reader:
        data = list(reader)
    new_data = []
    existing_urls = set()
    for _data in data:
        if "action_history" in _data.keys():
            if _data["website"] in existing_urls:
                continue
            else:
                if "No Operation" in " ".join(_data["action_history"][-2:]):
                    print("Should remove No Operation")
                    continue
                else:
                    new_data.append(_data)
                    existing_urls.add(_data["website"])
        else:
            print("No")
    print('len(existing_urls)',len(existing_urls))
    print("len(data)", len(data))
    print("len(filtered_data)", len(new_data))
    with jsonlines.open(file= file, mode="w") as writer:
        writer.write_all(new_data)



if __name__ == "__main__":
    parser = argparse.ArgumentParser('Red Team Web Agent')
    # parser.add_argument('--attack_type', choices=["action_grounding", "action_generation", "entire_query", "benign"])
    # parser.add_argument('--model_name', choices=["gpt4v", "gemini", "llava"])
    parser.add_argument('--file',default=None)
    args = parser.parse_args()
    
    file = args.file
    sanity_check_and_filter(file)