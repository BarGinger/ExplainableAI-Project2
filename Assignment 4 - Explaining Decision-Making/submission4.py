# Import necessary packages
from anytree import Node, RenderTree, AnyNode
from anytree.importer import DictImporter
from anytree.exporter import DotExporter
from anytree.search import find
from itertools import product
import json
import os
import numpy as np

print_mode = False

def find_starting_node(root, starting_node_name):
    """
    Traverse the tree to find the starting node by name.

    Parameters:
    root (Node): The root node of the tree
    starting_node_name (string): The name of the starting node to find

    return:
    Node: The starting node if found, otherwise None
    """
    node = find(root, lambda node: node.name == starting_node_name)
    if print_mode:
        if node:
            print(f"Node found: {node.name}")
        else:
            print("Node not found")

    return node

def generate_traces(node, calc_cost=False):
    """
    Recursively generates all possible traces from the given node.

    Parameters:
    node (Node): The current node in the tree
    calc_cost (bool): Whether to calculate the cost of each trace

    Returns:
    list: A list of all possible traces from the given node
    list: A list of the cost of each trace
    """
    if not hasattr(node, 'children') or not node.children:
        if calc_cost:
            return [[node.name]], [node.costs]  # Leaf node (ACT), end of a trace
        else:
            return [[node.name]], []  # Leaf node (ACT), end of a trace
    
    traces = []
    costs = []
    
    if node.type == "OR":
        # OR node: Select one child at a time
        for child in node.children:
            child_traces, child_cost = generate_traces(child, calc_cost)
            for trace in child_traces:
                traces.append([node.name] + trace)
            if calc_cost:
                for cost in child_cost:
                    costs.append(cost)
    
    elif node.type == "SEQ" or node.type == "AND":
        # SEQ/AND node: Concatenate traces of all children in order
        child_traces = []
        child_costs = []
        for child in node.children:
            child_traces_i, child_costs_i = generate_traces(child, calc_cost)
            child_traces.append(child_traces_i)
            child_costs.append(child_costs_i)
    
        for combination in product(*child_traces):
            traces.append([node.name] + [step for trace in combination for step in trace])
        
        if calc_cost:
            for combination in product(*child_costs):
                costs.append(np.sum([cost for cost in combination], axis=0))

    return traces, costs

def build_tree(json_node, parent=None):
    """
    Build the entire tree from the JSON object.

    Parameters:
    json_node (dict): The JSON object representing the tree
    parent (Node): The parent node

    Returns:
    Node: The root node of the tree
    """
    attributes = {k: v for k, v in json_node.items() if k not in ['name', 'type', 'children']}
    node = AnyNode(name=json_node['name'], type=json_node['type'], violation=False, parent=parent, **attributes)
    
    for child in json_node.get('children', []):
        build_tree(child, node)
    
    return node

def annotate_tree(node, norm):
    """
    Annotates the tree by marking nodes that violate the given norm.

    Parameters:
    node (Node): The current node in the tree
    norm (dict): The norm

    - If the norm is of type 'P' (prohibited), a node violates it if its name is in norm['actions'].
    - If the norm is of type 'O' (obligatory), a node violates it if it is an action but not in norm['actions'].
    """
    for child in node.children:
        annotate_tree(child, norm)

    if 'type' in norm:
        if norm['type'] == 'P':
            node.violation = node.name in norm['actions']
        elif norm['type'] == 'O':
            node.violation = node.name not in norm['actions'] and node.type == 'ACT'

    if hasattr(node, 'type') and node.type == 'OR':
        node.violation = all(child.violation for child in node.children)
    elif hasattr(node, 'type') and node.type in ['SEQ', 'AND']:
        node.violation = any(child.violation for child in node.children)

def export_tree_to_png(root, output_file):
    """
    Exports the tree to a PNG file with node properties.

    Parameters:
    root (Node): The root node of the tree
    output_file (string): The path to the output file
    """
    DotExporter(root, 
                nodeattrfunc=lambda node: f'label="{node.name}\nViolation: {node.violation}"'
               ).to_picture(output_file)

def main(json_tree, norm, goal, beliefs, preferences, output_dir=""):
    """
    Main function to determine the best execution trace for the agent.

    Parameters:
    json_tree (json object): The goal tree 
    norm (dict): The norm
    goal (list): The goal of the agent: a set of beliefs (strings) of the agent that must be true at the end of the execution of the trace.
    beliefs (list): A set of strings representing the initial beliefs of the agents.
    preferences (list): A pair describing the preference of the end-user.
    output_dir (string): The directory to save the output image

    Returns:
    output (list): A list of strings representing the execution trace chosen by the agent.
    """
    # Build the tree from the JSON object
    root = build_tree(json_tree)

    # Annotate the tree based on the given norm
    annotate_tree(root, norm)

    # Generating all possible traces of given tree, and calculating the cost of each trace
    traces, costs = generate_traces(root, calc_cost=True)

    if print_mode:
        print("costs: ", costs)
        print(f"Generated {len(traces)} traces:")
        for trace in traces:
            print(trace)

    # Filter traces that violate norms and keep their respective costs
    valid_traces = []
    valid_costs = []
    
    for trace, cost in zip(traces, costs):
        valid = True
        has_all_goals = [False for goal_belief in goal]
        agent_beliefs = beliefs.copy()

        for node_name in trace:
            node = find(root, lambda node: node.name == node_name)

            # check if node found
            if not node:
                continue

            if node.violation:
                valid = False
                if print_mode:
                    print(f"Trace violates norm: {trace}")
                break  

            if (node and hasattr(node, 'pre') and any(pre not in agent_beliefs for pre in node.pre)):
                valid = False
                if print_mode:
                    print(f"Trace violates beliefs: {trace}")
                    print(f"Current Agent Beliefs: {agent_beliefs}")
                    print(f"Node pre: {node.pre}")
                break

            # Update agent beliefs given me executed current node
            # add cuurent node post to agent beliefs
            if node and hasattr(node, 'post'):
                agent_beliefs.extend(node.post)

                # Check if all goals are achieved
                for i, goal_belief in enumerate(goal):
                    if hasattr(node, 'post') and goal_belief in node.post:
                        has_all_goals[i] = True

        if valid and all(has_all_goals):            
            valid_traces.append(trace)
            valid_costs.append(cost)

    # Sort traces based on user preferences.
    indices = preferences[1]
    sorted_traces_and_costs = sorted(zip(valid_traces, valid_costs), key=lambda x: tuple(x[1][i] for i in indices))
    valid_traces, valid_costs = zip(*sorted_traces_and_costs) if sorted_traces_and_costs else ([], [])

    # Return the best trace.
    output = valid_traces[0] if valid_traces else []
    if print_mode:
        print(f"Best trace: {output}")
    
    return output

output =  main(json_tree, norm, goal, beliefs, preferences)
