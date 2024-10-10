import os
import json
import shutil

import time
import google.api_core.exceptions
import google.generativeai as genai
from openai import OpenAI
from mistralai import Mistral
import ast
from botocore.exceptions import ClientError
import botocore
import boto3

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part


def create_json(file_path, title, text):
    json_object = {"title": title, "text": text}

    with open(file_path, "w", encoding='utf-8') as json_file:
        json.dump(json_object, json_file, ensure_ascii=False, indent=4)

def directory_creation(path_saving):
    if os.path.exists(path_saving):
        answer = input(f"Sure you want to delete the directory? {path_saving}: ")
        if answer == 'yes':
            shutil.rmtree(path_saving)
            os.makedirs(path_saving)
    else:
        os.makedirs(path_saving)

def gemini():
    def multiturn_generate_content():
        vertexai.init(project="66983676276", location="us-central1")
        model = GenerativeModel(
            "projects/66983676276/locations/us-central1/endpoints/3596371692571590656",
        )
        chat = model.start_chat()
        print(chat.send_message(
            ["""hey ciao come stai?"""],
            generation_config=generation_config,
            safety_settings=safety_settings
        ))


    generation_config = {
        "max_output_tokens": 8192,
        "temperature": 0,
        "top_p": 0.95,
    }

    safety_settings = [
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
        SafetySetting(
            category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=SafetySetting.HarmBlockThreshold.OFF
        ),
    ]

    multiturn_generate_content()

def openai():
    client = OpenAI(api_key='')

    try:
        response = client.chat.completions.create(
            # model="gpt-4o-mini-2024-07-18",
            model="ft:gpt-4o-mini-2024-07-18:personal::ADr6SnR3",
            response_format={"type": "json_object"},
            temperature=0,
            logprobs=True,
            messages=[{'role': 'system', 'content': 'You are a Cyber Threat Intelligence (CTI) analyst.'},
                      {'role': 'user', 'content': "Ciao come stai? Return the answer in the following json format {\"answer\": ""}"}]
        )

        print([response.choices[0].message, response.choices[0].logprobs])

    except Exception as e:
        print(f"Exception: ", e)

def mistral():
    client = Mistral("")

    print(client.models.list())

    chat_response = client.chat.complete(
        model="ft:mistral-large-latest:a2c174b0:20241002:f9986c34",
        messages=[{"role": 'user', "content": 'Hi, how are you?'}]
    )

    print(chat_response.choices[0].message.content)

def amazon():
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

    role = "Hi, how are you?"

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
        "temperature": 0,
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

if __name__ == '__main__':

    # openai()
    # gemini()
    mistral()
    # amazon()
