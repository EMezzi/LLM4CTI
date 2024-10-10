import os
import ast
import json
import re
import time
import boto3
import shutil
import pickle as pk
import vertexai
from langchain_community.llms import VLLM
from vertexai.generative_models import GenerativeModel, SafetySetting, Part
import botocore

from vertexai.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Part,
    SafetySetting,
)

from openai import OpenAI
from mistralai import Mistral
import google.api_core.exceptions
import google.generativeai as genai
from botocore.exceptions import ClientError
from miscellaneous.routine_functions import directory_creation


class GraphExtractor:

    @staticmethod
    def save_json(file_path, text):

        try:
            json_object = json.loads(text)
            print("Saving Json")

            with open(file_path, 'w') as json_file:
                print("Saving json")
                json.dump(json_object, json_file, indent=4)
        except Exception as e:
            print("Exception json: ", str(e), type(e))
            if """Expecting ',' delimiter""" in str(e):
                print("Eccola qui")


    @staticmethod
    def query_campaign_graph_openai(temperature, prompt, report):
        client = OpenAI(api_key='')

        try:
            response = client.chat.completions.create(
                #model="gpt-4o-mini-2024-07-18",
                model="ft:gpt-4o-mini-2024-07-18:personal::ADraZrz4",
                response_format={"type": "json_object"},
                temperature=temperature,
                logprobs=True,
                messages=[{'role': 'system', 'content': 'You are a Cyber Threat Intelligence (CTI) analyst.'},
                          {'role': 'user', 'content': prompt},
                          {'role': 'user', 'content': f'This is the Cyber Threat report {report}'}]
            )

            return [response.choices[0].message, response.choices[0].logprobs]

        except Exception as e:
            print(f"Exception: ", e)

    @staticmethod
    def query_campaign_graph_gemini(temperature, prompt, report):
        # genai.configure(api_key="")

        generation_config = {"temperature": temperature,
                             "max_output_tokens": 8192,
                             "response_mime_type": "application/json"}

        safety_settings = [
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=HarmBlockThreshold.OFF,
            ),
            SafetySetting(
                category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=HarmBlockThreshold.OFF,
            ),
        ]

        """
        safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_NONE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_NONE"
            },
        ]
        """

        vertexai.init(project="66983676276", location="us-central1")
        model = GenerativeModel(model_name="projects/66983676276/locations/us-central1/endpoints/3019488727803101184",
                                generation_config=generation_config)

        """
        model = genai.GenerativeModel(model_name="projects/66983676276/locations/us-central1/endpoints/3019488727803101184",
                                      generation_config=generation_config,
                                      safety_settings=safety_settings)
        """

        correct = False

        try:
            response = model.generate_content(contents=['You are a Cyber Threat Intelligence (CTI) analyst.',
                                                        prompt,
                                                        f'This is the Cyber Threat report {report}'])
            try:
                answer = response.text
                correct = True

            except Exception as e:
                print("Exception 1: ", e)
                answer = "Failed to generate a response."

        except google.api_core.exceptions.InternalServerError:
            print("Google Internal server error")
            answer = "Failed to generate a response."

        except google.api_core.exceptions.RetryError:
            print("Retry error")
            answer = "Failed to generate a response."

        except google.api_core.exceptions.ResourceExhausted:
            time.sleep(60)
            try:
                response = model.generate_content(contents=prompt, request_options={"timeout": 1000})
                answer = response.text
                correct = True
                print("Ciao")
            except google.api_core.exceptions.InternalServerError:
                print("Internal server error")
                answer = "Failed to generate a response."
            except ValueError:
                print("Value error")
                answer = "Failed to generate a response."
            except Exception as e:
                print("Exception 2: ", e)
                answer = "Failed to generate a response."

        except google.generativeai.types.generation_types.StopCandidateException:
            print("Stop candidate Exception")
            answer = "Failed to generate a response."

        except Exception as e:
            print("Exception 3: ", e)
            answer = "Failed to generate a response."

        if correct:
            return answer
        else:
            return "Failed to generate a response"

    @staticmethod
    def query_campaign_graph_mistral(temperature, prompt, report):
        api_key, model = "", "mistral-large-latest"

        client = Mistral(api_key=api_key)

        try:

            chat_response = client.chat.complete(
                model="ft:mistral-large-latest:a2c174b0:20241002:0f447fbd",
                temperature=temperature,
                response_format={"type": "json_object"},
                messages=[{'role': 'system', 'content': 'You are a Cyber Threat Intelligence (CTI) analyst.'},
                          {'role': 'user', 'content': prompt},
                          {'role': 'user', 'content': f'This is the Cyber Threat report {report}'}]
            )

            return chat_response.choices[0].message.content

        except Exception as e:
            print("Mistral Exception: ", e)

    @staticmethod
    def query_campaign_graph_llama(temperature, prompt, report):
        """ Query the Llama model to generate fixes."""

        config = botocore.config.Config(
            read_timeout=900,
            connect_timeout=900
        )

        # Initialize the Amazon Bedrock runtime client
        client = boto3.client(
            aws_access_key_id="",
            aws_secret_access_key="",
            service_name="bedrock-runtime",
            region_name="us-west-2",
            config=config
        )

        def extract_json(response):
            json_start = response.index("{")
            json_end = response.rfind("}")
            return response[json_start:json_end + 1]

        model_id = "meta.llama3-1-70b-instruct-v1:0"

        role = 'You are a Cyber Threat Intelligence (CTI) analyst.\n'
        prompt += f"""\nThis is the Cyber Threat report {report}"""
        role += prompt

        # Embed the prompt in Llama 3's instruction format.
        formatted_prompt = f"""
            <|begin_of_text|>
            <|start_header_id|>user<|end_header_id|>
            {role}
            <|eot_id|>
            <|start_header_id|>assistant<|end_header_id|>
            """

        # Format the request payload using the model's native structure.
        native_request = {
            "prompt": formatted_prompt,
            "temperature": temperature,
        }

        # Convert the native request to JSON.
        request = json.dumps(native_request)

        try:
            # Invoke the model with the request.
            response = client.invoke_model(modelId=model_id, body=request)

            dict_str = response["body"].read().decode("UTF-8")
            answer_dict = ast.literal_eval(dict_str)

            answer = answer_dict['generation']
            answer = extract_json(answer)

            # input_tokens = answer["prompt_token_count"]
            # output_tokens = answer["generation_token_count"]

            return answer

        except (ClientError, Exception) as e:
            print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")


    @staticmethod
    def main_campaign_graph(files_path, path_saving, path_saving_logits, sampled, temperature, prompt, model):
        """
        :param files_path: path where there are the dataset files.
        :param saving_path: path where the inferred graphs are saved.
        :param temperature: temperature parameter for the gpt model.
        :param prompt: necessary prompt for the gpt model.
        :return:
        """

        directory_creation(path_saving)

        if path_saving_logits != "":
            directory_creation(path_saving_logits)

        for i, report in enumerate(sampled):
            print("Report: ", i, report)
            with open(f'{files_path}/{report}', 'rb') as file:
                json_file = json.load(file)

                title = json_file['pdf_title']

                print("The title is: ", title)

                if len(title) == 1:
                    with open(f'/Users/manu/PycharmProjects/LlmTI/datasets/pdf_json/{title[0][:-4]}.json',
                              'rb') as file2:
                        json_file2 = json.load(file2)
                        text = json_file2['text']

                        answer = None
                        if model == "gpt-4o-mini-2024-07-18":
                            pair = GraphExtractor.query_campaign_graph_openai(temperature, prompt, text)
                            answer = pair[0]

                            if path_saving_logits != "":
                                logprobs = pair[1]

                                with open(f'{path_saving_logits}/{report[:-5]}.pk', 'wb') as probs_file:
                                    pk.dump(logprobs, probs_file)

                        elif model == "gemini":
                            answer = GraphExtractor.query_campaign_graph_gemini(temperature, prompt, text)
                        elif model == "mistral":
                            print("Hey")
                            answer = GraphExtractor.query_campaign_graph_mistral(temperature, prompt, text)
                        elif model == "llama":
                            answer = GraphExtractor.query_campaign_graph_llama(temperature, prompt, text)

                        try:
                            if type(answer) is str:
                                print("Answer is: ", answer)
                                answer = re.sub(r"\'", '\"', answer)
                                GraphExtractor.save_json(f'{path_saving}/{report}', answer)
                            else:
                                print("Answer IS: ", answer)
                                GraphExtractor.save_json(f'{path_saving}/{report}', answer.content)
                        except Exception as e:
                            print("Exception in the last part: ", e)
