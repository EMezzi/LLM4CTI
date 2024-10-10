import json
import os
import pandas as pd
import numpy as np
from transformers import RobertaModel, AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import ast
from openai import OpenAI
import pickle as pk

from sentence_transformers import SentenceTransformer, util


def check_file_vuln(title):
    for file in sorted(os.listdir("../datasets/campaign_graph")):
        with open(f"../datasets/campaign_graph/{file}", "rb") as json_file:
            json_object = json.load(json_file)

            if title in json_object["pdf_title"]:
                print("file name: ", file)


def check_names(check, mod, model, graph_type):
    if check == 'validation':
        for i in range(1):
            for j in range(2):
                print(f"Temperature: {i}, Prompt: {j}")
                dir =  f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/{graph_type}/{check}/second_version/{mod}/{model}/comb_{i}_{j}'
                dataset_dir = f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/{graph_type}'
                files = os.listdir(dir)
                for file in files:
                    # print("File: ", file)
                    with open(f'{dir}/{file}', 'rb') as json_file:
                        json_object = json.load(json_file)

                        attack_vect_names = [attack_vector['name'].lower() for attack_vector in json_object['nodes']['attack_vector']]

                        if graph_type == 'campaign_graph':
                            if len(json_object['nodes']['campaign']) > 1 or len(json_object['nodes']['APT']) > 1 \
                                    or "(" in json_object['nodes']['campaign'][0]['actor'] \
                                    or ")" in json_object['nodes']['campaign'][0]['actor'] \
                                    or "/" in json_object['nodes']['campaign'][0]['actor'] \
                                    or "N/A" in json_object['nodes']['campaign'][0]['actor'].lower() \
                                    or " or " in json_object['nodes']['campaign'][0]['actor'][0].lower():
                                    # or "unknown" in json_object['nodes']['campaign'][0]['actor'].lower():
                                    print("Guilty: ", file)
                                    with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                        json_object_set = json.load(dataset_json)
                                        print("Campaign actor: ", json_object_set['nodes']['campaign'][0]['actor'], json_object_set['nodes']['campaign'][0]['date_start'])
                                        print("APT: ", json_object_set['nodes']['APT'][0]['name'])
                                        print("Vectors: ", json_object_set['nodes']['attack_vector'])
                                        print("\n")

                        elif graph_type == 'context_graph':
                            if len(json_object['nodes']['APT']) > 1 \
                                    or "(" in json_object['nodes']['APT'][0]['name'] \
                                    or ")" in json_object['nodes']['APT'][0]['name'] \
                                    or "/" in json_object['nodes']['APT'][0]['name'] \
                                    or " or " in json_object['nodes']['APT'][0]['name'][0].lower():
                                print("Guilty: uao", file)
                                with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                    json_object_set = json.load(dataset_json)
                                    print("APT: ", json_object_set['nodes']['APT'][0]['name'])

                            if len(json_object['nodes']['country']) > 1:
                                print("Guilty: ", file)
                                with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                    json_object_set = json.load(dataset_json)
                                    print("Country: ", json_object_set['nodes']['country'])

    elif check == 'test':
        for i in range(1):
            print("Temperature: ", i)
            for j in range(10):
                print("Iteration: ", j)

                dir = f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/{graph_type}/{check}/second_version/{mod}/{model}/comb_{i}/3_{j}'
                dataset_dir = f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/{graph_type}'
                files = os.listdir(dir)

                for file in files:
                    # print("File: ", file)
                    with open(f'{dir}/{file}', 'rb') as json_file:
                        json_object = json.load(json_file)

                        if graph_type == 'campaign_graph':
                            if len(json_object['nodes']['campaign']) > 1 or len(json_object['nodes']['APT']) > 1 or \
                                    "(" in json_object['nodes']['campaign'][0]['actor'] or \
                                    ")" in json_object['nodes']['campaign'][0]['actor'] or \
                                    "/" in json_object['nodes']['campaign'][0]['actor'] or \
                                    "N/A" in json_object['nodes']['campaign'][0]['actor'][0].lower() or \
                                    " or " in json_object['nodes']['campaign'][0]['actor'][0].lower():
                                    #"unknown" in json_object['nodes']['campaign'][0]['actor'].lower():

                                    print("Guilty: ", file)
                                    with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                        json_object_set = json.load(dataset_json)
                                        print("Campaign actor: ", json_object_set['nodes']['campaign'][0]['actor'],
                                              json_object_set['nodes']['campaign'][0]['date_start'])
                                        print("APT: ", json_object_set['nodes']['APT'][0]['name'])
                                        print("\n")

                        elif graph_type == 'context_graph':
                            if len(json_object['nodes']['APT']) > 1 \
                                    or "(" in json_object['nodes']['APT'][0]['name'] \
                                    or ")" in json_object['nodes']['APT'][0]['name'] \
                                    or "/" in json_object['nodes']['APT'][0]['name'] \
                                    or " or " in json_object['nodes']['campaign'][0]['actor'][0].lower():
                                print("Guilty: uao", file)
                                with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                    json_object_set = json.load(dataset_json)
                                    print("APT: ", json_object_set['nodes']['APT'][0]['name'])

                            if len(json_object['nodes']['country']) > 1:
                                print("Guilty: ", file)
                                with open(f'{dataset_dir}/{file}', 'rb') as dataset_json:
                                    json_object_set = json.load(dataset_json)
                                    print("Country: ", json_object_set['nodes']['country'])



def check_dates(check):
    if check == 'validation':
        for i in range(2):
            for j in range(4):
                print(f"Temperature: {i}, Prompt: {j}")
                dir = f'/Users/manu/PycharmProjects/LlmTI/inferring/campaign_graph/validation/comb_{i}_{j}'
                files = os.listdir(dir)
                for file in files:
                    with open(f'{dir}/{file}', 'rb') as json_file:
                        json_object = json.load(json_file)
                        dates = json_object['nodes']['campaign'][0]['date_start']

                        for date in dates:
                            if len(date.split('-')) > 2:
                                print(date)
    elif check == 'test':
        for i in range(2):
            for j in range(4):
                print(f"Temperature: {i}, Iteration: {j}")
                for file in os.listdir(
                        f'/Users/manu/PycharmProjects/LlmTI/inferring/campaign_graph/test/comb_{i}/3_{j}'):
                    with open(
                            f'/Users/manu/PycharmProjects/LlmTI/inferring/campaign_graph/test/comb_{i}/3_{j}/{file}',
                            'rb') as json_file:
                        json_object = json.load(json_file)

                        dates = json_object['nodes']['campaign'][0]['date_start']

                        for date in dates:
                            if len(date.split('-')) > 2:
                                print(date)


def check_equality():
    for i in range(2):
        print(f"Temperature: {i}")
        for file in os.listdir(
                f'/Users/manu/PycharmProjects/LlmTI/inferring/campaign_graph/validation/comb_{i}_3'):
            with open(f'/Users/manu/PycharmProjects/LlmTI/inferring/campaign_graph/validation/comb_{i}_3/{file}',
                      'rb') as json_file:
                print(f"File: {file}")
                json_object = json.load(json_file)

                if json_object['nodes']['campaign'][0]['actor'] != json_object['nodes']['APT'][0]['name']:
                    print("Campaign actor: ", json_object['nodes']['campaign'][0]['actor'])
                    print("Actor name: ", json_object['nodes']['APT'][0]['name'])


def check_ground_truth_names():
    for file in sorted(os.listdir(
            f'/Users/manu/PycharmProjects/LlmTI/datasets/campaign_graph/')):
        with open(f'/Users/manu/PycharmProjects/LlmTI/datasets/campaign_graph/{file}', 'rb') as json_file:
            print(f"File: {file}")
            json_object = json.load(json_file)

            print(json_object['nodes']['campaign'][0]['actor'])
            print(json_object['nodes']['APT'][0]['name'])
            print("\n")


def check_similarity(check):
    if check == 'validation':
        df_file = pd.read_excel(
            f"/Users/manu/PycharmProjects/LlmTI/results/campaign_graph/metrics/{check}/results_0_3.xlsx")

        df_file['sim_APT'] = df_file['sim_APT'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
        df_file['sim_APT'] = df_file['sim_APT'].str[0]

        print(df_file['sim_APT'])

        print(len(df_file[df_file['sim_APT'] < 0.80]['sim_APT']))

    elif check == 'test':
        for temperature in [0, 1]:
            print("Temperature: ", temperature)
            for i in range(10):
                print("Iteration: ", i)
                df_file = pd.read_excel(
                    f"/Users/manu/PycharmProjects/LlmTI/results/campaign_graph/metrics/{check}/results_{temperature}_3_{i}.xlsx")

                df_file['sim_APT'] = df_file['sim_APT'].apply(lambda x: ast.literal_eval(x) if pd.notna(x) else x)
                df_file['sim_APT'] = df_file['sim_APT'].str[0]

                print(len(df_file[df_file['sim_APT'] < 0.80]['sim_APT']))


def check_vulnerability():
    vulnerability_column = list(df_final['vulnerability'].str.lower())
    attack = list(set([vuln for vuln in vulnerability_column if not vuln.startswith('cve')]))

    print("All the attacks: ", attack)


def check_secondary_source():
    df_final = pd.read_excel(
        '/Users/manu/PycharmProjects/LlmTI/data_preprocessing/discard_pdfs/rel_threatactor_vulnerabilities_final.xlsx')

    secondary = df_final.drop_duplicates(subset=["name", "date_start"])
    print(secondary['secondary source pdf'].count())
    print(secondary['secondary source'].count())

def check_goals_labels():

    dir = '/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph'
    files_context = os.listdir(dir)

    goals = []
    labels = []
    for file in files_context:
        with open(f'{dir}/{file}', 'rb') as json_file:
            print("File: ", file)
            json_graph = json.load(json_file)
            print(json_graph["nodes"]["APT"][0]["name"])
            print("Labels: ", json_graph["nodes"]["APT"][0]["labels"])
            print("Goals: ", json_graph["nodes"]["APT"][0]["goals"])
            goals.append(json_graph["nodes"]["APT"][0]["goals"])
            labels.append(json_graph["nodes"]["APT"][0]["labels"])

    print(list(set(goals)))
    print(list(set(labels)))

def check_exchange_labels_goals():

    for model in ['gpt-4o-mini-2024-07-18', 'gemini', 'mistral']:
        for temp in [0, 1]:
            for prompt in [0]:
                dir = f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/validation/second_version/{model}/comb_{temp}_{prompt}'
                files = os.listdir(dir)
                for file in files:
                    print("File: ", file)
                    with open(f'{dir}/{file}', 'rb') as json_file:
                        json_graph = json.load(json_file)

                        labels = json_graph["nodes"]["APT"][0]["labels"]
                        json_graph["nodes"]["APT"][0]["labels"] = json_graph["nodes"]["APT"][0]["goals"]
                        json_graph["nodes"]["APT"][0]["goals"] = labels

                        print(json_graph["nodes"]["APT"][0]["labels"])
                        print(json_graph["nodes"]["APT"][0]["goals"])

                        with open(f'{dir}/{file}', 'w') as json_file1:
                            json.dump(json_graph, json_file1, indent=4)

def add_nodes_key(task, model, i, j):
    path = f"/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/{task}/validation/second_version/normal/{model}/comb_{i}_{j}"

    files = os.listdir(path)

    for file in files:
        with open(f"{path}/{file}", "rb") as json_file:
            json_object = json.load(json_file)

            with open(f"{path}/{file}", "w") as json_file1:
                json.dump(json_object, json_file1, indent=4)

def check_difference_zero_few(task, model):
    path_zero = f"/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/{task}/validation/second_version/normal/{model}/comb_0_0"
    path_few = f"/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/{task}/validation/second_version/normal/{model}/comb_0_1"

    files_zero = os.listdir(path_zero)

    for file_zero in files_zero:
        json_zero = json.load(open(f"{path_zero}/{file_zero}", "r"))
        json_few = json.load(open(f"{path_few}/{file_zero}", "r"))

        cve_zero = json_zero["nodes"]["vulnerability"]
        cve_few = json_few["nodes"]["vulnerability"]

        attack_vectors_zero = json_zero["nodes"]["attack_vector"]
        attack_vectors_few = json_few["nodes"]["attack_vector"]

        if cve_zero != cve_few:
            print("cve_zero: ", cve_zero)
            print("cve_few:", cve_few)
            print("Different for cve")

        if attack_vectors_zero != attack_vectors_few:
            print("attack zero: ", attack_vectors_zero)
            print("attack few: ", attack_vectors_few)
            print("Different for attack vectors")



if __name__ == '__main__':
    check_difference_zero_few("campaign_graph", "mistral")
