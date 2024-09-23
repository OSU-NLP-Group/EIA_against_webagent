import requests
import sys

port = sys.argv[1] if len(sys.argv) > 1 else 8000



url = f"http://127.0.0.1:{port}/webpages/000c2828-e8ce-4b18-bfe0-89ed333add06/7dcf08f4-e760-4be7-be8c-0a533074883e/adv_modified_file_action_generation_form_type1_near_top_0.html"
response = requests.get(url)




print("Content:", response.text)
print("Status Code:", response.status_code)