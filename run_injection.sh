
subtypes=("form_type0" "form_type1" "form_type2" "copy")
positions=("near_bot_2" "near_bot_1" "near_top_1" "near_top_2" "near_top_0" "near_bot_0" "most_top" "most_bot")

echo "Starting Action Grounding"

# Action Grounding
for subtype in "${subtypes[@]}"
do
    for position in "${positions[@]}"
    do
        python ./injection/generate_malicious_html.py --attack_type action_grounding --attack_subtype "$subtype" --attack_position "$position"
    done
done

echo "Starting Action Generation"

# Action Generation
for position in "${positions[@]}"
do
    python ./injection/generate_malicious_html.py --attack_type action_generation --attack_subtype "form_type1" --attack_position "$position"
done

echo "Script finished successfully"