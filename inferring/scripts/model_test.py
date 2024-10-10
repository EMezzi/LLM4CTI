import os
import json
import pickle as pk
from functools import reduce
import operator

import numpy as np

from openai_campaign import GraphExtractor
from variables import grid_search, grid_search_infer, json_campaign_test, json_context_test
from graph_alignment import GraphAligner
from openai_context import llm_infer_context
from data_preprocessing.scripts.preprocessing_json import Preprocessor
from results.scripts.metrics_calculation import MetricsCalculator


def bootstrapping(key, values):

    resampled_means = {'pr': [], 'rec': [], 'f1': []}

    for i in range(1000):
        index = np.random.randint(10, size=6)
        precision_values = [values[key]['pr'][i] for i in index]
        recall_values = [values[key]['rec'][i] for i in index]
        f1_values = [values[key]['f1'][i] for i in index]

        resampled_means['pr'].append(np.mean(precision_values))
        resampled_means['rec'].append(np.mean(recall_values))
        resampled_means['f1'].append(np.mean(f1_values))

    bounds = {'pr': {'lower': None, 'upper': None}, 'rec': {'lower': None, 'upper': None},
              'f1': {'lower': None, 'upper': None}}

    for metric in resampled_means.keys():
        bounds[metric]['lower'] = round(np.percentile(resampled_means[metric], 5), 2)
        bounds[metric]['upper'] = round(np.percentile(resampled_means[metric], 95), 2)

    return bounds

def contains_any_substring(word1, word2):
    # Generate all possible substrings of word2
    for i in range(len(word2)):
        for j in range(i + 1, len(word2)):
            substring = word2[i:j]
            if substring in word1:
                return True

    return False

def access_logprobs(path_logits, modality):

    files = os.listdir(path_logits)

    # confidence_per_file_category = {}

    if modality == 'campaign_graph':
        for file in files[:10]:
            print("File: ", file)
            # confidence_per_file_category[file] = {}
            with (open(f'{path_logits}/{file}', 'rb') as logits_object):
                logits = pk.load(logits_object).content
                logits = [logit for logit in logits if logit.token != '{' and logit.token != '}' and logit.token != '"'
                          and logit.token != '{\n' and logit.token != ' "' and logit.token != '":' and logit.token != '       '
                          and logit.token != '   ' and logit.token != ' {\n' and logit.token != ' [\n' and logit.token != '           '
                          and logit.token != '               ' and logit.token != '",\n' and logit.token != ' ["' and logit.token != '"],\n'
                          and logit.token != ' }\n' and logit.token != ' ]\n' and logit.token != '"\n' and logit.token != ' ],\n'
                          and logit.token != 'nodes' and logit.token != 'date' and logit.token != '_start']

                print(logits)

                i = 0
                n_logits = len(logits)

                confidence_per_file_category = {}
                while i < n_logits:
                    if logits[i].token == 'campaign' and logits[i + 1].token != '1':
                        print(logits[i].token, logits[i + 1].token)
                        # confidence_per_file_category[file]['campaign'] = []
                        confidence_per_file_category['campaign'] = []
                        while logits[i + 1].token != 'id':
                            i += 1
                            confidence_per_file_category['campaign'].append([logits[i].token, np.exp(logits[i].logprob)])

                    elif logits[i].token == 'APT' and logits[i + 1].token != '1':
                        print(logits[i].token, logits[i + 1].token)
                        confidence_per_file_category['APT'] = []
                        while logits[i + 1].token != 'id':
                            i += 1
                            confidence_per_file_category['APT'].append([logits[i].token, np.exp(logits[i].logprob)])
                    else:
                        i += 1

                print(confidence_per_file_category)
                for category in ['campaign', 'APT']:
                    second_elements = [sublist[1] for sublist in confidence_per_file_category[category]]
                    result = reduce(operator.mul, second_elements)
                    print(f"Confidence {category}: ", result)


    if modality == 'context_graph':
        dict_grouping = {'APT': [], 'country': [], 'vulnerability': []}
        for file in files:
            #print("File: ", file)

            with (open(f'{path_logits}/{file}', 'rb') as logits_object):
                logits = pk.load(logits_object).content
                logits = [logit for logit in logits if logit.token != '{' and logit.token != '}' and logit.token != '"'
                          and logit.token != '{\n' and logit.token != ' "' and logit.token != '":' and logit.token != '       '
                          and logit.token != '   ' and logit.token != ' {\n' and logit.token != ' [\n' and logit.token != '           '
                          and logit.token != '               ' and logit.token != '",\n' and logit.token != ' ["' and logit.token != '"],\n'
                          and logit.token != ' }\n' and logit.token != ' ]\n' and logit.token != '"\n' and logit.token != ' ],\n'
                          and logit.token != 'nodes' and logit.token != 'date' and logit.token != '_start' and logit.token != '     ' and logit.token != 'name'
                          and logit.token != ' },\n']

                #print(logits)
                i = 0
                n_logits = len(logits)

                confidence_per_file_category = {}
                while i < n_logits:
                    if logits[i].token == 'APT' and logits[i + 1].token != '1':
                        #print(logits[i].token, logits[i + 1].token)
                        confidence_per_file_category['APT'] = []
                        while logits[i + 1].token != 'id' and logits[i + 1].token != 'go':
                            i += 1
                            confidence_per_file_category['APT'].append([logits[i].token, np.exp(logits[i].logprob)])

                    elif logits[i].token == 'country' and logits[i + 1].token != '1':
                        #print(logits[i].token, logits[i + 1].token)
                        confidence_per_file_category['country'] = []
                        while logits[i + 1].token != 'id':
                            i += 1
                            confidence_per_file_category['country'].append([logits[i].token, np.exp(logits[i].logprob)])

                    elif logits[i].token == 'ulnerability' and logits[i + 1].token != '1':
                        #print(logits[i].token, logits[i + 1].token)
                        confidence_per_file_category['vulnerability'] = []
                        while i < n_logits:
                            confidence_per_file_category['vulnerability'].append([logits[i].token, np.exp(logits[i].logprob)])
                            i += 1
                    else:
                        i += 1

                #print(confidence_per_file_category)
                for category in ['APT', 'country', 'vulnerability']:
                    second_elements = [sublist[1] for sublist in confidence_per_file_category[category]]
                    result = reduce(operator.mul, second_elements)
                    dict_grouping[category].append(result)
                    # print(f"Confidence {category}: ", result)

        print("mean confidence country: ", np.mean(dict_grouping['country']))
        print("mean confidence vulnerability: ", np.mean(dict_grouping['vulnerability']))



def check_difference(temp, i, model, files_ref, graph_type, logits_mode):

    if logits_mode == "":
        files_ref = set(files_ref)
        files_test = set(os.listdir(f'../../inferring/{graph_type}/test/second_version/{mod}/{model}/comb_{temp}{logits_mode}/3_{i}'))
        diff = list(files_ref - files_test)

        return diff

    else:
        files_ref = set([file[:-5] for file in files_ref])
        files_test = set([file[:-3] for file in os.listdir(f'../../inferring/{graph_type}/test/second_version/{mod}/{model}/comb_{temp}{logits_mode}/3_{i}')])

        diff = list(files_ref - files_test)
        return diff

models = ["gpt-4o-mini-2024-07-18", "gemini"] #"mistral"]
modality = ['fine_tuned']

if __name__ == '__main__':

    ga = GraphAligner()

    choice = 'context'

    if choice == 'campaign':
        for mod in modality:
            for model in models:
                print("Model: ", model)
                for temperature in grid_search['temperature'][:1]:
                    print("Temperature: ", temperature)
                    list_d = []
                    print("Prompt: ", grid_search['prompts'][0])
                    for i in range(0, 10):
                        json_to_repeat = check_difference(temperature, i, model, json_campaign_test, 'campaign_graph', "")
                        logits_to_repeat = check_difference(temperature, i, model, json_campaign_test, 'campaign_graph', "_logits")

                        print(json_to_repeat)
                        print(logits_to_repeat)

                        """
                        GraphExtractor.main_campaign_graph(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                           f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}',
                                                           f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/test/second_version/{mod}/{model}/comb_{temperature}_logits/3_{i}',
                                                           json_to_repeat, temperature, grid_search['prompts'][0], model)
                        """

                        """
                        access_logprobs(f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/test/second_version/{mod}/{model}/comb_{temperature}_logits/3_{i}', 'campaign_graph')
                        """

                        """
                        Preprocessor.preprocess_json_campaign_graph(f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}')
                        """

                        """
                        ga.main_graph_alignment(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/similarities/second_version/{mod}/{model}/test/comb_{temperature}/3_{i}')
                        """

                        """
                        Preprocessor.build_csv_from_json_similarities(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/similarities/second_version/{mod}/{model}/test/comb_{temperature}/3_{i}',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/metrics/second_version/{mod}/{model}/test/results_{temperature}_3_{i}.xlsx',
                                                                      choice)
                        """

                        MetricsCalculator.main_metrics(f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/metrics/second_version/{mod}/{model}/test/results_{temperature}_3_{i}.xlsx',
                                                       list_d, choice, 0.80, 0.00, temperature, i)

                    main_dict = {}
                    keys = ['campaign', 'APT', 'vulnerability', 'vector', 'attr_to', 'targets', 'employs']
                    for key in keys:
                        main_dict[key] = {}
                        main_dict[key]['pr'], main_dict[key]['rec'], main_dict[key]['f1'], main_dict[key]['sim'] = [], [], [], []
                        for i, d in enumerate(list_d):
                            main_dict[key]['pr'].append(d[(temperature, i, 0.8)][key]['pr'])
                            main_dict[key]['rec'].append(d[(temperature, i, 0.8)][key]['rec'])
                            main_dict[key]['f1'].append(d[(temperature, i, 0.8)][key]['f1'])

                    metrics = ['pr', 'rec', 'f1']
                    for key in keys:
                        for metric in metrics:
                            print(f"Key: {key}, Metric: {metric}, Min: {min(main_dict[key][metric])}, Max: {max(main_dict[key][metric])}")

                    for key in keys:
                        print(key.upper())
                        bounds = bootstrapping(key, main_dict)
                        print(bounds)

    elif choice == 'context':

        for mod in modality:
            for model in models:
                print("Model: ", model)
                for temperature in grid_search['temperature'][:1]:
                    print("Temperature: ", temperature)
                    list_d = []
                    print("Prompt: ", grid_search_infer['prompts'][0])

                    for i in range(0, 10):
                        json_to_repeat = check_difference(temperature, i, model, json_context_test, 'context_graph', "")
                        logits_to_repeat = check_difference(temperature, i, model, json_context_test, 'context_graph', "_logits")

                        print(json_to_repeat)
                        print(logits_to_repeat)

                        """
                        llm_infer_context(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                          f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}',
                                          f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/test/second_version/{mod}/{model}/comb_{temperature}_logits/3_{i}',
                                          json_to_repeat, temperature, grid_search_infer['prompts'][0], model)
                        """

                        """
                        access_logprobs(
                            f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/test/second_version/{mod}/{model}/comb_{temperature}_logits/3_{i}',
                            'context_graph')
                        """

                        """
                        Preprocessor.preprocess_json_context(f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}')
                        """

                        """
                        ga.main_graph_alignment(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/test/second_version/{mod}/{model}/comb_{temperature}/3_{i}',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/similarities/second_version/{mod}/{model}/test/comb_{temperature}/3_{i}')
                        """

                        """
                        Preprocessor.build_csv_from_json_similarities(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/similarities/second_version/{mod}/{model}/test/comb_{temperature}/3_{i}',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/metrics/second_version/{mod}/{model}/test/results_{temperature}_3_{i}.xlsx',
                                                                      choice)
                        """

                        MetricsCalculator.main_metrics(f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/metrics/second_version/{mod}/{model}/test/results_{temperature}_3_{i}.xlsx',
                                                       list_d, choice, 0.80, 0.00, temperature, i)


                    print(list_d)
                    main_dict = {}
                    keys = ['APT', 'country', 'goals', 'labels', 'vulnerability', 'vector', 'origin', 'targets', 'uses']
                    for key in keys:
                        main_dict[key] = {}
                        main_dict[key]['pr'], main_dict[key]['rec'], main_dict[key]['f1'], main_dict[key]['sim'] = [], [], [], []
                        for i, d in enumerate(list_d):
                            main_dict[key]['pr'].append(d[(temperature, i, 0.8)][key]['pr'])
                            main_dict[key]['rec'].append(d[(temperature, i, 0.8)][key]['rec'])
                            main_dict[key]['f1'].append(d[(temperature, i, 0.8)][key]['f1'])

                    print("Main dict: ", main_dict)

                    for key in keys:
                        print(key.upper())
                        bounds = bootstrapping(key, main_dict)
                        print(bounds)