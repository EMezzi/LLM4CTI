import os
import json

import numpy as np

models = ['gpt-4o-mini-2024-07-18', 'gemini', 'mistral']
temperatures = [0, 1]
prompts = [0, 1, 2, 3]

def check_difference(mod):

    if mod == "validation":
        for temp in temperatures:
            print("Temperature: ", temp)
            for prompt in prompts:
                print("Prompt: ", prompt)
                files_ref = set(os.listdir(f'../campaign_graph/validation/openai/comb_{temp}_{prompt}'))
                for model in models:
                    files_test = set(os.listdir(f'../campaign_graph/validation/{model}/comb_{temp}_{prompt}'))

                    # elements in openai but not in another model
                    diff = list(files_ref - files_test)

                    print(f"Difference between openai and {model}: ", diff)

    elif mod == "test":
        for temp in temperatures:
            print("Temperature: ", temp)
            for i in range(10):
                print(f"Iteration: {i}")
                files_ref = set(os.listdir(f'../campaign_graph/test/openai/comb_{temp}/3_{i}'))
                for model in models:
                    files_test = set(os.listdir(f'../campaign_graph/test/{model}/comb_{temp}/3_{i}'))

                    diff = list(files_ref - files_test)

                    print(f"Difference between openai and {model}: ", diff)




check_difference("test")


