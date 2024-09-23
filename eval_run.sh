
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# EIA
# Objective: Leak user specific PII
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 



# Mirror Injection
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_copy_near_bot_2"



# Form Injection (aria)
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type1_near_bot_2"



# Form Injection (text)
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type0_near_bot_2"



# Mirror Injection + Systemsive defensive prompt

python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_grounding_copy_near_bot_2"



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# EIA
# Objective: Leak full user request
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 


#  evaluate the ASR
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_2"


#  evaluate the ASR_o

python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_most_top" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_most_bot" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_0" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_1" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_top_2" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_0" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_1" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_grounding_form_type2_near_bot_2" --injected_element_only


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Relaxed-EIA
# Objective: Leak full user request
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Evaluate the ASR
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_2"

#  evaluate the ASR_o
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_most_top" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_most_bot" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_0" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_1" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_top_2" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_0" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_1" --injected_element_only
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results/gpt4v/action_generation_form_type1_near_bot_2" --injected_element_only

# Evaluate the ASR + Defensive System Prompt
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_most_top"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_most_bot"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_top_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_top_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_top_2"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_bot_0"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_bot_1"
python eval.py --eval_dir_benign "eval_results/eval_results/gpt4v/benign" --eval_dir "eval_results/eval_results_with_system_defense/gpt4v/action_generation_form_type1_near_bot_2"