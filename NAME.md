This file provides the description of the arguments we used in this repo and how they map to the settings in our paper.


1. attack type: action grounding
    
    - copy : mirror injection

    - form type0 : form injection (text)

    - form type1 : form injection (aria)

        All of them above are set to leak the specific PII.

    - form type2: using the same injection strategy as form injection (text). However, the opacity of the injection is still zero, but the injected instruction is for **leaking full request** instead of the specific PII.


2. attack type: action generation

    The opacity of the injection is set to 0.2 to affect both the action generation and grounding compoments. The persuasive prompt is set to leak the full request.

    - form type1 : form injection (text)

3. positions

    | Arugments    | Positions in paper      |
    |------------|-------------|
    | most top   | $P_{+\infty}$      |
    | near_top_2 | $P_{+3}$      |
    | near_top_1 | $P_{+2}$      |
    | near_top_0 | $P_{+1}$      |
    | near_bot_0 | $P_{-1}$     |
    | near_bot_1 | $P_{-2}$      |
    | near_bot_2 | $P_{-3}$      |
    | most bot   | $P_{-\infty}$      |