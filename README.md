# EIA: ENVIRONMENTAL INJECTION ATTACK ON GENERALIST WEB AGENTS FOR PRIVACY LEAKAGE

This is the official repo of EIA ([https://arxiv.org/abs/2409.11295](https://arxiv.org/abs/2409.11295)). If you find it helpful, please kindly 🌟star🌟 it and cite our paper 📜.

![EIA_overview](attack_overview_new.png)

EIA is a form of indirect prompt injection, but specifically designed to manipulate the environment where state-changing actions occur, with a particular focus on exploiting
the web environment to target generalist web agents.

Specifically, it injects web elements along with malicious (yet seemingly benign, see figure) instructions into the HTML of the benign website. The injected elements and the instructions are both set to be invisible on the website. This manipulation misleads the web agent into entering private information into the injected elements, thus causing the leakage of the user’s private data. 

Overall, EIA achieves up to 70% ASR to steal user specific PII and 16% ASR to leak the full user request. We also demonstrate that EIA can not be detected by traditional web malware detection tool, [VirusTotal](https://www.virustotal.com/gui/home/upload), and won't affect the agent's next step towards completing the user tasks (ASR_pt). Additionally, an extra defensive system prompt can not mitigate the risks of EIA.

## Environmental Setup
Our experimental environment mainly follows the setup of [SeeAct](https://github.com/OSU-NLP-Group/SeeAct). Specifically, we utilized the version of commit `472be0434c54896e2ee0a009d71169a4884da677` which you can assess at [here](https://github.com/OSU-NLP-Group/SeeAct/tree/472be0434c54896e2ee0a009d71169a4884da677), and upgrade the version of `openai` to `1.33.0`.

### Dataset
In our work, we deditecately select tasks from [Mind2Web](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file) and manually adapt the corresponding realistic website from the provided raw dump file (such as populating the necessary information). After filtering out instances with low quality, we ultimately finalize a set of 177 action steps containing PII and their corresponding webpages.


### Download
You can download the webpages with injection directly via the Globus as well.
For more information and overview of Globus , please refer to [here](https://github.com/OSU-NLP-Group/Mind2Web?tab=readme-ov-file#raw-dump-with-full-traces-and-snapshots) and [here](https://www.osc.edu/resources/getting_started/howto/howto_use_globus_overview).

You can access the `data.zip` folder under the link below:
```python
Data Download: https://app.globus.org/file-manager?origin_id=6e0b9952-da25-4b74-a4f9-7450f0bb96b9&origin_path=%2F
```

After download the `data.zip`, unzip the file and place it under the repo folder. The folder should look like:
```
data
├── webpages_filtered
├──── <annotation_id>
├────── <action_id>
├── target_element_HTML.json
├── all_instances.jsonl
```
where the `webpages_filtered` folder contains the webpages for web agent to operate.
`all_instances.jsonl` contains the overview of the tasks encompassing the user private information. `target_element_HTML.json` contains the html content of the target element for each instances. It is used to help us locate the $P_0$ position (reference point) of the target element and further inject the malicious elements into different positions according to the reference point.

### EIA
The `injection` folder contains code for injecting various EIA attacks into benign webpages. As detailed in our paper, this includes different types of injections targeting either the action grounding stage or the action generation stage, each serving different purposes.

To perform the injection, simply run the following command:

```./run_injection.sh```

### Website Deployment
To setup the website and make them accessible by SeeAct via HTTP connection, run the code:
```python
cd web/
uvicorn main:app --reload --port 8000
```
where you can customize your own port number.

You can test if the connection is established by running:
```python
python web_request_test.py
```
which will print out the status code. 200 means you setup successfully.



### Run SeeAct over the webpage
We cover all the experiments we have in the `SeeAct/EIA_run.sh` with comments.
You can also read the NAME.md file to better know how the arguments map to the setting in our paper.


### Evaluation results over three LMMs.
We also provide the evaluation results from the same link above with the name `eval_results.zip`. 

> [!NOTE]
> to replicate the results within the `eval_results_w_defensive_system_prompt` folder, please uncomment the lines [here](https://github.com/OSU-NLP-Group/EIA/blob/9a300399ae5e497c4c6e993b68b3e4a88977be6f/SeeAct/src/data_utils/prompts.py#L358).

### Evaluation
Please refer to `eval_run.sh` to get the ASR, ASR_o and ASR_pt results.


## Citation
If you find the paper and any resources here helpful, pls kindly cite our paper:
```
@article{liao2024eia,
  title={EIA: Environmental Injection Attack on Generalist Web Agents for Privacy Leakage},
  author={Liao, Zeyi and Mo, Lingbo and Xu, Chejian and Kang, Mintong and Zhang, Jiawei and Xiao, Chaowei and Tian, Yuan and Li, Bo and Sun, Huan},
  journal={arXiv preprint arXiv:2409.11295},
  year={2024}
}
```
