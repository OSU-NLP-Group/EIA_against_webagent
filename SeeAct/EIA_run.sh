

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# EIA
# Objective: Leak user specific PII
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

# Form Injection (text)
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_bot_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_bot_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_top_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_top_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_top_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position near_bot_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type0 --attack_position most_top --model_name gpt4v --save_dir "../eval_results/eval_results"

# Form Injection (aria)
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_bot_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_bot_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_top_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_top_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_top_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position near_bot_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type1 --attack_position most_top --model_name gpt4v --save_dir "../eval_results/eval_results"

# Mirror Injection
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_bot_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_bot_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_top_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_top_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_top_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position near_bot_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype copy --attack_position most_top --model_name gpt4v --save_dir "../eval_results/eval_results"


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# EIA
# Objective: Leak full user request
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_bot_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_bot_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_top_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_top_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_top_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position near_bot_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_grounding --attack_subtype form_type2 --attack_position most_top --model_name gpt4v --save_dir "../eval_results/eval_results"



# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# Relaxed-EIA
# Objective: Leak full user request
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_bot_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_bot_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_top_1 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_top_2 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_bot_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position near_top_0 --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position most_top --model_name gpt4v --save_dir "../eval_results/eval_results"
python main.py --attack_type action_generation --attack_subtype form_type1 --attack_position most_bot --model_name gpt4v --save_dir "../eval_results/eval_results"
