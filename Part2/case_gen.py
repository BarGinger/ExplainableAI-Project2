import json
import random
import csv
from itertools import product
from anytree import AnyNode
from anytree.importer import DictImporter

with open("coffee.json", "r") as file:
    json_data = json.load(file)

def build_tree(json_node, parent=None):
    attributes = {k: v for k, v in json_tree.items() if k not in ['name', 'type','children']}
    node = AnyNode(id=json_tree['id'], name=json_tree['name'], parent=parent)
    node = AnyNode(name=json_node['name'], type=json_node['type'], parent=parent, **attributes)
    
    for child in json_node.get('children', []):
        build_tree(child, node)
    
    return node

# Function to generate all valid execution traces
def generate_traces(node, beliefs, trace=[]):
    if node.type == "ACT":
        # Check if all preconditions are met
        if hasattr(node, "pre") and not all(pre in beliefs for pre in node.pre):
            return []  # Cannot execute this action
        
        # Execute the action: Add postconditions to beliefs
        new_beliefs = beliefs.copy()
        if hasattr(node, "post"):
            new_beliefs.update(node.post)
        
        return [[trace + [node.name]], new_beliefs]  # Return trace
    
    traces = []
    if node.type in ["SEQ", "AND"]:
        new_beliefs = beliefs.copy()
        child_traces = []
        
        for child in node.children:
            child_trace, new_beliefs = generate_traces(child, new_beliefs, trace)
            if not child_trace:
                return []  # If any step fails, return no valid trace
            child_traces.append(child_trace)
        
        for combination in product(*child_traces):
            traces.append(trace + [step for sub_trace in combination for step in sub_trace])
    
    elif node.type == "OR":
        for child in node.children:
            child_trace, new_beliefs = generate_traces(child, beliefs, trace)
            if child_trace:
                traces.append(trace + child_trace)
    
    return traces

# Function to generate random norms, beliefs, and preferences
def generate_random_case():
    possible_beliefs = ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney", "AnnInOffice"]
    possible_norms = ["payShop", "getOthersCard", "gotoKitchen", "gotoShop"]
    
    beliefs = random.sample(possible_beliefs, random.randint(3, 5))
    norm = {"type": random.choice(["P", "O"]), "actions": [random.choice(possible_norms)]}
    preferences = [["quality", "price", "time"], random.sample([0, 1, 2], 3)]
    
    return beliefs, norm, preferences

# Function to generate 500 training cases and save to CSV
def generate_training_cases(filename, num_cases=500):
    root = build_tree(json_tree)
    
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["norm", "beliefs", "goal", "preferences", "executed_actions", "action_to_explain"])
        
        for _ in range(num_cases):
            beliefs, norm, preferences = generate_random_case()
            goal = ["haveCoffee"]
            action_to_explain = random.choice(["payShop", "getOwnCard", "gotoKitchen", "gotoShop"])
            
            # Generate execution trace
            traces = generate_traces(root, set(beliefs))
            if traces:
                executed_actions = traces[0]  # Pick the first valid trace
            else:
                executed_actions = []
            
            # Write to CSV
            writer.writerow([json.dumps(norm), json.dumps(beliefs), json.dumps(goal), 
                             json.dumps(preferences), json.dumps(executed_actions), action_to_explain])

# Run the case generator
generate_training_cases("training_data.csv", num_cases=500)
print("500 training cases saved to training_data.csv")
