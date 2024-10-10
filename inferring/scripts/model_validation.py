import pandas as pd
import numpy as np
import json
import ast
import os

from variables import grid_search, grid_search_infer, json_campaign_validation, prompt_dates, json_context_validation
from data_preprocessing.scripts.preprocessing_json import Preprocessor
from results.scripts.metrics_calculation import MetricsCalculator
from openai_context import llm_infer_context
from openai_campaign import GraphExtractor
from graph_alignment import GraphAligner
import google.generativeai as genai
import google.api_core.exceptions


def avg_dict_filling(list_d, keys_cat):
    avg_dict = {}

    for d in list_d:
        for key in d.keys():
            avg_dict[key] = {}
            avg_dict[key]['pr'], avg_dict[key]['rec'], avg_dict[key]['f1'], avg_dict[key]['sim'] = [], [], [], []
            for key_cat in keys_cat:
                avg_dict[key]['pr'].append(d[key][key_cat]['pr'])
                avg_dict[key]['rec'].append(d[key][key_cat]['rec'])
                avg_dict[key]['f1'].append(d[key][key_cat]['f1'])
                avg_dict[key]['sim'].append(d[key][key_cat]['sim'])

            avg_dict[key]['pr'] = round(np.mean(avg_dict[key]['pr']), 2)
            avg_dict[key]['rec'] = round(np.mean(avg_dict[key]['rec']), 2)
            avg_dict[key]['f1'] = round(np.mean(avg_dict[key]['f1']), 2)
            avg_dict[key]['sim'] = round(np.mean(avg_dict[key]['sim']), 2)

    return avg_dict

# models = ['mistral']#'gpt-4o-mini-2024-07-18', 'gemini']
models = ['gpt-4o-mini-2024-07-18', 'llama']
modality = ['normal']

def check_difference(files_to_check, task, val_test, mod, model, temp, prompt):
    files_test = set(os.listdir(f'../../inferring/{task}/{val_test}/second_version/{mod}/{model}/comb_{temp}_{prompt}'))
    diff = list(set(files_to_check) - files_test)

    print(f"Difference between openai and {model}: ", diff, len(diff))

    return diff

if __name__ == '__main__':
    # json_files = os.listdir('/Users/manu/PycharmProjects/LlmTI/inferring/inferred_json_graphs/campaign_graph/')
    # sampled = random.sample(json_files, 174)

    ga = GraphAligner()

    choice = 'context'

    if choice == 'campaign':
        for mod in modality:
            for model in models:
                list_d = []
                print("Model: ", model)
                for i, temperature in enumerate(grid_search['temperature'][:1]):
                    print("Temperature: ", temperature)
                    for j, prompt in enumerate(grid_search['prompts']):
                        print("Prompt: ", prompt)

                        """
                        json_campaign_remaining = check_difference(files_to_check=json_campaign_validation,
                                                                   task="campaign_graph",
                                                                   val_test="validation",
                                                                   mod=mod, model=model, temp=i, prompt=j)
                        """

                        """
                        GraphExtractor.main_campaign_graph('/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                           f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}',
                                                           "",
                                                           json_campaign_validation, temperature, prompt, model)
                        """

                        """
                        Preprocessor.preprocess_json_campaign_graph(f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}')
                        """

                        """
                        ga.main_graph_alignment(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/campaign_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/similarities/second_version/{mod}/{model}/validation/comb_{i}_{j}')
                        """

                        """
                        Preprocessor.build_csv_from_json_similarities('/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/campaign_graph',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/similarities/second_version/{mod}/{model}/validation/comb_{i}_{j}',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/metrics/second_version/{mod}/{model}/validation/results_{i}_{j}.xlsx',
                                                                      choice)
                        """

                        MetricsCalculator.main_metrics(f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/campaign_graph/metrics/second_version/{mod}/{model}/validation/results_{i}_{j}.xlsx',
                                                       list_d, choice, 0.80, 0, i, j)

                for d in list_d:
                    print(d)
                
    elif choice == 'context':

        for mod in modality:
            for model in models:
                print("Model: ", model)
                list_d = []
                for i, temperature in enumerate(grid_search_infer['temperature'][:1]):
                    print("Temperature: ", temperature)
                    for j, prompt in enumerate(grid_search_infer['prompts']):
                        print("Prompt: ", prompt)

                        """
                        json_context_remaining = check_difference(files_to_check=json_context_validation,
                                                                   task="context_graph",
                                                                   val_test="validation",
                                                                   mod=mod, model=model, temp=i, prompt=j)

                        print(json_context_remaining)
                        """

                        """
                        llm_infer_context('/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                          f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}',
                                          "",
                                          json_context_remaining, temperature, prompt, model)
                        """

                        """
                        Preprocessor.preprocess_json_context(f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}')
                        """

                        """
                        ga.main_graph_alignment('/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/inferring/context_graph/validation/second_version/{mod}/{model}/comb_{i}_{j}',
                                                f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/similarities/second_version/{mod}/{model}/validation/comb_{i}_{j}')
                        """

                        """
                        Preprocessor.build_csv_from_json_similarities(f'/Users/manu/Documents/GitHub/LLMPipe4TI/datasets/context_graph',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/similarities/second_version/{mod}/{model}/validation/comb_{i}_{j}',
                                                                      f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/metrics/second_version/{mod}/{model}/validation/results_{i}_{j}.xlsx', choice)
                        """

                        MetricsCalculator.main_metrics(f'/Users/manu/Documents/GitHub/LLMPipe4TI/results/context_graph/metrics/second_version/{mod}/{model}/validation/results_{i}_{j}.xlsx', list_d, choice, 0.80, 0.00, i, j)
                        
                        
                for d in list_d:
                    print(d)












