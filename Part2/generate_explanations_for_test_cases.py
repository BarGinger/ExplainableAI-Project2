"""
Generate explanations for the inputs test cases
"""

import pandas as pd
import json
import os
from naive_baseline import generate_naive_baseline
from utils import generate_formal_explanations

def generate_explanations_for_inputs(test_cases):
    """
    Generate explanations for the inputs test cases
    :param test_cases: dictionary containing the test cases
    :return: dictionary containing the explanations for each test case
    """
    current_dir = os.path.dirname(__file__)
    explanations_dir = os.path.join(current_dir, "explanations", "baseline")
    os.makedirs(explanations_dir, exist_ok=True)
    
    explanations = {}
    for index, row in test_cases.iterrows():
        # Read the JSON file into a dictionary
        with open(f'{current_dir}/{row["name_json_tree_file"]}', 'r') as file:
            json_tree = json.load(file)
        # Generate formal explanations
        formal_explentions, chosen_trace = generate_formal_explanations(json_tree=json_tree, norm=row["norm"], beliefs=row["beliefs"], goal=row["goal"], preferences=row["preferences"], action_to_explain=row["action_to_explain"])
        explanations[index] = generate_naive_baseline(formal_explentions=formal_explentions, chosen_trace=chosen_trace, norm=row["norm"], beliefs=row["beliefs"], goal=row["goal"], preferences=row["preferences"], action_to_explain=row["action_to_explain"])
        
        # Save each explanation to a separate text file
        explanation_file = os.path.join(explanations_dir, f"{index}.txt")
        with open(explanation_file, 'w') as f:
            for explanation in explanations[index]:
                f.write(explanation + '\n')
    
    return explanations

if __name__ == '__main__':
    current_dir = os.path.dirname(__file__)
    explanations_dir_baseline = os.path.join(current_dir, "explanations", "baseline")
    os.makedirs(explanations_dir_baseline, exist_ok=True)



    test_cases = [
        {
            "name_json_tree_file": "coffee.json",
            "norm": {"type": "P", "actions": ["payShop"]},
            "beliefs": ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney", "AnnInOffice"],
            "goal": ["haveCoffee"],
            "preferences": [["quality", "price", "time"], [1, 2, 0]],
            "action_to_explain": "payShop"
        },
        {
            "name_json_tree_file": "coffee.json",
            "norm": {},
            "beliefs": ["staffCardAvailable", "ownCard"],
            "goal": ["haveCoffee"],
            "preferences": [["quality", "price", "time"], [0, 1, 2]],
            "action_to_explain": "getCoffeeKitchen"
        },
        {
            "name_json_tree_file": "coffee.json",
            "norm": {},
            "beliefs": ["haveMoney", "AnnInOffice"],
            "goal": ["haveCoffee"],
            "preferences": [["quality", "price", "time"], [0, 1, 2]],
            "action_to_explain": "getCoffeeShop"
        },
        {
            "name_json_tree_file": "coffee.json",
            "norm": {"type": "P", "actions": ["gotoAnnOffice"]},
            "beliefs": ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney", "AnnInOffice"],
            "goal": ["haveCoffee"],
            "preferences": [["quality", "price", "time"], [0, 1, 2]],
            "action_to_explain": "payShop"
        },
        {
            "name_json_tree_file": "coffee.json",
            "norm": {"type": "P", "actions": ["payShop"]},
            "beliefs": ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney"],
            "goal": ["haveCoffee"],
            "preferences": [["quality", "price", "time"], [1, 2, 0]],
            "action_to_explain": "gotoKitchen"
        }
    ]

    df_test_cases = pd.DataFrame(test_cases, index=[f"test_case_{i+1}" for i in range(len(test_cases))])

    explanations = generate_explanations_for_inputs(df_test_cases)

    print("all explanations have been generated and saved to the explanations folder")