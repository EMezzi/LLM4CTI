import re
import ast
import json
import time
import boto3
import vertexai
import pickle as pk
from openai import OpenAI
from mistralai import Mistral
import google.api_core.exceptions
import google.generativeai as genai
from botocore.exceptions import ClientError
from miscellaneous.routine_functions import directory_creation

from vertexai.generative_models import (
    GenerativeModel,
    HarmCategory,
    HarmBlockThreshold,
    Part,
    SafetySetting,
)


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


def query_context_apt_openai(apt_name, description, temperature, prompt):
    client = OpenAI(api_key='')

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            # model="ft:gpt-4o-mini-2024-07-18:personal::ADr6SnR3",
            response_format={"type": "json_object"},
            temperature=temperature,
            logprobs=True,

            messages=[{'role': 'system', 'content': 'You are a Cyber Threat Intelligence (CTI) analyst.'},
                      {'role': 'user', 'content': prompt},
                      {'role': 'user', 'content': f'Name of the APT: {apt_name}. Description of the APT: {description}'}]
        )

        return [response.choices[0].message, response.choices[0].logprobs]

    except Exception as e:
        print(f"Exception: ", e)

def query_context_apt_gemini(apt_name, description, temperature, prompt):
    genai.configure(api_key='')

    generation_config = {"temperature": temperature,
                         "max_output_tokens": 8192,
                         "response_mime_type": "application/json"}

    safety_settings = [
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HARASSMENT,
            threshold=HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_HATE_SPEECH,
            threshold=HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
            threshold=HarmBlockThreshold.BLOCK_NONE,
        ),
        SafetySetting(
            category=HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
            threshold=HarmBlockThreshold.BLOCK_NONE,
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

    model = GenerativeModel(
        model_name="projects/66983676276/locations/us-central1/endpoints/3596371692571590656",
        generation_config=generation_config,
    )

    correct = False

    try:
        response = model.generate_content(contents=['You are a Cyber Threat Intelligence (CTI) analyst.',
                                                    prompt,
                                                    f'Name of the APT: {apt_name}. Description of the APT: {description}'])
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


def query_context_mistral(apt_name, description, temperature, prompt):
    api_key, model = '', "mistral-large-latest"

    client = Mistral(api_key=api_key)

    try:
        chat_response = client.chat.complete(
            model="ft:mistral-large-latest:a2c174b0:20241002:f9986c34",
            temperature=temperature,
            response_format={"type": "json_object"},
            messages=[{'role': 'system', 'content': 'You are a Cyber Threat Intelligence (CTI) analyst.'},
                      {'role': 'user', 'content': prompt},
                      {'role': 'user', 'content': f'Name of the APT: {apt_name}. Description of the APT: {description}'}]
        )

        return chat_response.choices[0].message.content

    except Exception as e:
        print("Mistral Exception: ", e)

def query_context_llama(apt_name, description, temperature, prompt):
    """ Query the Llama model to generate fixes."""

    # Initialize the Amazon Bedrock runtime client
    client = boto3.client(
        aws_access_key_id='',
        aws_secret_access_key='',
        service_name="bedrock-runtime",
        region_name="us-west-2"
    )

    def extract_json(response):
        json_start = response.index("{")
        json_end = response.rfind("}")
        return response[json_start:json_end + 1]

    model_id = "meta.llama3-1-70b-instruct-v1:0"

    role = 'You are a Cyber Threat Intelligence (CTI) analyst.\n'
    prompt += f'Name of the APT: {apt_name}. Description of the APT: {description}'
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


def llm_infer_context(path_dataset, path_saving, path_saving_logits, sampled_context, temperature, prompt, model):
    """
    :return:
    """

    directory_creation(path_saving)

    if path_saving_logits != "":
        directory_creation(path_saving_logits)

    for json_graph in sampled_context:
        print(json_graph)
        with open(f'{path_dataset}/{json_graph}', 'rb') as file:
            json_file = json.load(file)

            # One query version
            apt_name = json_file["nodes"]["APT"][0]["name"]
            apt_description = json_file["nodes"]["APT"][0]["description"]

            answer = None
            if model == "gpt-4o-mini-2024-07-18":
                pair = query_context_apt_openai(apt_name, apt_description, temperature, prompt)
                answer = pair[0]

                if path_saving_logits != "":
                    logprobs = pair[1]

                    with open(f'{path_saving_logits}/{json_graph[:-5]}.pk', 'wb') as probs_file:
                        pk.dump(logprobs, probs_file)

            elif model == "gemini":
                answer = query_context_apt_gemini(apt_name, apt_description, temperature, prompt)
            elif model == "mistral":
                answer = query_context_mistral(apt_name, apt_description, temperature, prompt)
            elif model == "llama":
                answer = query_context_llama(apt_name, apt_description, temperature, prompt)

            try:
                if type(answer) is str:
                    print("Answer is: ", answer)
                    answer = re.sub(r"\'", '\"', answer)
                    save_json(f'{path_saving}/{json_graph}', answer)
                else:
                    print("Answer IS: ", answer)
                    save_json(f'{path_saving}/{json_graph}', answer.content)
            except Exception as e:
                print("Exception in the last part: ", e)
