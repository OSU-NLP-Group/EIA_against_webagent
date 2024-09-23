# -*- coding: utf-8 -*-
# Copyright (c) 2024 OSU Natural Language Processing Group
#
# Licensed under the OpenRAIL-S License;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.licenses.ai/ai-pubs-open-rails-vz1
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import os
import time
import base64
import google.generativeai as genai
import PIL.Image

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

class Engine:
    def __init__(self) -> None:
        pass

    def tokenize(self, input):
        return self.tokenizer(input)


class GeminiEngine(Engine):
    def __init__(
            self,
            api_key,
            stop=["\n\n"],
            rate_limit=30,
            model=None,
            temperature=0,
            seed=42,
            **kwargs,
    ) -> None:
        """Init an OpenAI GPT/Codex engine

        Args:
            api_key (_type_, optional): Auth key from OpenAI. Defaults to None.
            stop (list, optional): Tokens indicate stop of sequence. Defaults to ["\n"].
            rate_limit (int, optional): Max number of requests per minute. Defaults to -1.
            model (_type_, optional): Model family. Defaults to None.
        """
        self.api_keys = [api_key]
        self.stop = stop
        self.temperature = temperature
        self.model = genai.GenerativeModel(model)
        # convert rate limit to minmum request interval
        self.request_interval = 0 if rate_limit == -1 else 60.0 / rate_limit
        self.next_avil_time = [0] * len(self.api_keys)
        self.current_key_idx = 0
        self.seed = seed
        Engine.__init__(self, **kwargs)

    def renew_chat(self):
        self.chat = self.model.start_chat(history = [])
        
    def generate(self, prompt: list = None, max_new_tokens=4096, temperature=None, model=None, image_path=None,
                 ouput__0=None, turn_number=0, **kwargs):

        start_time = time.time()
        if (
                self.request_interval > 0
                and start_time < self.next_avil_time[self.current_key_idx]
        ):
            time.sleep(self.next_avil_time[self.current_key_idx] - start_time)
            
        system_prompt = prompt[0]
        action_generation_prompt = prompt[1]
        grounding_prompt = prompt[2]

        if turn_number == 0:
            self.renew_chat()

            img = PIL.Image.open(image_path)
            # prompt1 = "SYSTEM: " + system_prompt + self.stop[0] + "USER: <image>" + self.stop[0] + action_generation_prompt + self.stop[0] + "ASSISTANT:"
            prompt1 = system_prompt + self.stop[0] +  action_generation_prompt
            # response1 = self.model.generate_content([prompt1, img], stream=True)
            response1 = self.chat.send_message([prompt1, img])
            response1.resolve()

            answer1 = response1.text

            return answer1

        elif turn_number == 1:
            # img = PIL.Image.open(image_path)
            # prompt2 = "SYSTEM: " + system_prompt + self.stop[0] + "USER: " + self.stop[0] + action_generation_prompt + self.stop[0] + "ASSISTANT: " + ouput__0 + self.stop[0] + "USER: <image>" + grounding_prompt + self.stop[0] + "ASSISTANT: "
            
            # response2 = self.model.generate_content([prompt2, img], stream=True)
            response2 = self.chat.send_message(grounding_prompt)
            # response2.resolve()

            answer2 = response2.text
            return answer2

