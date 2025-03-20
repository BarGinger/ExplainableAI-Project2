"""
HW2.4. Practice - Assignment 4 - Explaining Decision-Making
Write an algorithm to explain why a certain action was executed as part of a selected execution trace. The selected execution trace should be selected according to assignment 3.

Please, refer to the Project description on Blackboard for all the details and instructions of the assignment.

The setup code gives the following variables:

Name	Type	Description
json_tree	json object	The goal tree
norm	dict	The norm
goal	list	The goal of the agent: a set of beliefs (strings) of the agent that must be true at the end of the execution of the trace.
beliefs	list	A set of strings representing the initial beliefs of the agents.
preferences	list	A pair describing the preference of the end-user.
action_to_explain	string	The name of the action to explain
Your code snippet should define the following variables:

Name	Type	Description
selected_trace	list	A list of strings representing the execution trace chosen by the agent. The strings in the list are the names of the nodes in the execution trace.
output	list	An explanation in the form of a list of lists. If the action is not in the trace, return an empty list, otherwise the explanation should contain a list of explanatory factors
Instructions:
A file coffee.json is provided as input for the exercise and pre-loaded for you in the variable json_tree.
For this variant of the exercise, the variables have the following values:

Variable	Value
norm	{'type': 'P', 'actions': ['gotoKitchen']}
goal	['haveCoffee']
beliefs	['staffCardAvailable', 'ownCard']
preferences	[['quality', 'price', 'time'], [1, 2, 0]]
action_to_explain	"getOthersCard"
After saving and grading this variant, press the New Variant button to try a different variant.

Explanations format and explanatory factors: please see the detailed Project description on Blackboard.
Given a request to explain action_to_explain from a trace 
, the explanation is expected to be empty if action_to_explain is not part of 
. Otherwise, it is expected that the explanation contains

For each OR node,
One "C" factor for the selected alternative for the OR node that led to action_to_explain
An explanation for each alternative not selected, either via a "V" factor, an "N" factor, or a "F" factor explanation, depending on the reason. Note: if, for one alternative not selected, multiple reasons are true, only report the first factor, considering the order above (i.e., a "V" factor only if no "N" factor is relevant, and a "F" factor only if no "N" nor "V" factors are releant).
For each ACT node executed before (and including) action_to_explain, one "P" factor explanation.
For each node linked by action_to_explain (if any), one or more (based on the chain of links) "L" factor explanations.
For each parent of action_to_explain, if it is a goal node (either OR or AND or SEQ), one "D" factor explanation
Each explanatory factor should be represented as a list where the first element of a list is a string representing the type of factor (denoted with a letter prefix) and the rest of the list contains relevant informations for the explanatory factor, as explained in the Project description.
"""

from anytree import AnyNode
from anytree.exporter import DotExporter
from anytree.search import find
from anytree import PreOrderIter
from itertools import product
import json
import os
import numpy as np

print_mode = False

def find_node(root, node_to_find):
    """
    Traverse the tree to find the starting node by name.

    Parameters:
    root (Node): The root node of the tree
    node_to_find (string): The name of the node to find

    return:
    Node: The starting node if found, otherwise None
    """
    node = find(root, lambda node: node.name == node_to_find)
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
    node (Node): The current node in the tree.
    calc_cost (bool): Whether to calculate the cost of each trace.

    Returns:
    list: A list of all possible traces from the given node.
    list: A list of the cost of each trace.
    """
    # If the node has no children, it is a leaf node (ACT), end of a trace
    if not hasattr(node, 'children') or not node.children:
        if calc_cost:
            return [[node.name]], [node.costs]
        else:
            return [[node.name]], []

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
            # Recursively generate traces and costs for each child
            child_traces_i, child_costs_i = generate_traces(child, calc_cost)
            child_traces.append(child_traces_i)
            child_costs.append(child_costs_i)

        # Generate all combinations of traces from children
        for combination in product(*child_traces):
            traces.append([node.name] + [step for trace in combination for step in trace])

        if calc_cost:
            # Sum the costs for each combination of child traces
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
    # Extract attributes from the JSON node, excluding 'name', 'type', and 'children'
    attributes = {k: v for k, v in json_node.items() if k not in ['name', 'type', 'children']}
    
    # Create a new node with the extracted attributes
    node = AnyNode(name=json_node['name'], type=json_node['type'], violation=False, parent=parent, **attributes)
    
    # Recursively build the tree for each child node
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
    # Recursively annotate each child node
    for child in node.children:
        annotate_tree(child, norm)

    # Check if the current node violates the norm
    if 'type' in norm:
        if norm['type'] == 'P':
            # Prohibited norm: node violates if its name is in norm['actions']
            node.violation = node.name in norm['actions']
        elif norm['type'] == 'O':
            # Obligatory norm: node violates if it is an action but not in norm['actions']
            node.violation = node.name not in norm['actions'] and node.type == 'ACT'

    # For OR nodes, the node violates if all children violate
    if hasattr(node, 'type') and node.type == 'OR':
        node.violation = all(child.violation for child in node.children)
    # For SEQ/AND nodes, the node violates if any child violates
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

def make_decision(json_tree, norm, goal, beliefs, preferences, output_dir=""):
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
    tree (Node): The root node of the tree
    chosen_trace (list): A list of strings representing the execution trace chosen by the agent.
    valid_traces (list): A list of all valid traces
    valid_costs (list): A list of the cost of each valid trace
    """
    # Build the tree from the JSON object
    root = build_tree(json_tree)

    # Annotate the tree based on the given norm
    annotate_tree(root, norm)

    # Generate all possible traces of the given tree, and calculate the cost of each trace
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

            # Check if node found
            if not node:
                continue

            # Check if the node violates any norms
            if node.violation:
                valid = False
                if print_mode:
                    print(f"Trace violates norm: {trace}")
                break  

            # Check if the node violates any preconditions
            if (node and hasattr(node, 'pre') and any(pre not in agent_beliefs for pre in node.pre)):
                valid = False
                if print_mode:
                    print(f"Trace violates beliefs: {trace}")
                    print(f"Current Agent Beliefs: {agent_beliefs}")
                    print(f"Node pre: {node.pre}")
                break

            # Update agent beliefs given the execution of the current node
            if node and hasattr(node, 'post'):
                agent_beliefs.extend(node.post)

                # Check if all goals are achieved
                for i, goal_belief in enumerate(goal):
                    if hasattr(node, 'post') and goal_belief in node.post:
                        has_all_goals[i] = True

        # If the trace is valid and all goals are achieved, add it to the valid traces
        if valid and all(has_all_goals):            
            valid_traces.append(trace)
            valid_costs.append(cost)

    # Sort traces based on user preferences
    if preferences and len(preferences) == 2:
        indices = preferences[1]
        sorted_traces_and_costs = sorted(zip(valid_traces, valid_costs), key=lambda x: tuple(x[1][i] for i in indices))
        valid_traces, valid_costs = zip(*sorted_traces_and_costs) if sorted_traces_and_costs else ([], [])

    # Return the best trace
    chosen_trace = valid_traces[0] if valid_traces else []
    if print_mode:
        print(f"Best trace: {chosen_trace}")
    
    return root, chosen_trace, valid_traces, valid_costs


def create_explanation(key="", node_name=None, value=[]):
    """
    Creates an explanation for a given key, node name, and value.

    Parameters:
    key (string): The key of the explanation
    node_name (string): The name of the node
    value (list): The value of the explanation

    Returns:
    list: A list representing the explanation
    """
    # Convert each element in the value list to a string, including arrays
    # formatted_value = []
    # if key not in ['U']:
    #     for v in value:
    #         if isinstance(v, list):
    #             formatted_value.append(v)
    #         else:
    #             formatted_value.append(str(v))
    # else:
    #     formatted_value = value

    if node_name is None:
        return [key] + value
    
    return [key, node_name] + value


def add_explanation(explanations, key="", node_name=None, value=[]):
    """
    Adds an explanation to the list of explanations.

    Parameters:
    explanations (list): The list of explanations
    key (string): The key of the explanation
    node_name (string): The name of the node
    value (list): The value of the explanation
    """
    explanations.append(create_explanation(key, node_name, value))

def get_cost_of_node(traces, costs, node):
    """
    Calculate the cost of a given node.

    Parameters:
    traces (list): A list of all possible traces
    costs (list): A list of the cost of each trace
    node (Node): The node for which to calculate the cost

    Returns:
    list: The cost of the node
    """
    if not traces or not costs or not node:
        return []
    
    if hasattr(node, 'costs'):
        return node.costs

    # Find the index of the node in the traces
    node_index = next((i for i, trace in enumerate(traces) if node.name in trace), None)

    # If the node is not found in the traces, return an empty list
    if node_index is None:
        return []
    
    # Return the cost of the node
    return costs[node_index]

def add_linked_node_explanations(explanations, node, root):
     if hasattr(node, 'link') and node.link:
        for dest_node_name in node.link:
            linked_node = find_node(root, dest_node_name)
            if linked_node:
                add_explanation(explanations, key='L', node_name=node.name, value=['->', dest_node_name])
            if hasattr(linked_node, 'link') and node.link:
                add_linked_node_explanations(explanations, linked_node, root)



def generate_explanations(json_tree, norm, goal, beliefs, preferences, action_to_explain, output_dir=""):
    """
    Explain why a certain action was executed as part of a selected execution trace

    Parameters:
    json_tree (json object): The goal tree 
    norm (dict): The norm
    goal (list): The goal of the agent: a set of beliefs (strings) of the agent that must be true at the end of the execution of the trace.
    beliefs (list): A set of strings representing the initial beliefs of the agents.
    preferences (list): A pair describing the preference of the end-user.
    action_to_explain (string): The name of the action to explain.
    output_dir (string): The directory to save the output image

    Returns:
    output (list): A list of strings representing the execution trace chosen by the agent.
    chosen_trace (list): A list of strings representing the execution trace chosen by the agent.
    """

    explanations = []

    # Use part 3 code to get selected trace - Get the root node, the chosen trace, and the valid traces
    root, chosen_trace, valid_traces, valid_costs = make_decision(json_tree, norm, goal, beliefs, preferences, output_dir)


    print(f"Chosen trace: {chosen_trace}")
    if not chosen_trace or len(chosen_trace) == 0 or action_to_explain not in chosen_trace:
        print(f"Action to explain: {action_to_explain} not in trace")
        # If the action is not in the trace, return an empty list
        return [], chosen_trace
    else:
        print(f"Action to explain: {action_to_explain} in trace")


    # Get target node to explain
    target_node = find_node(root, action_to_explain)
    if not target_node:
        return [], chosen_trace

    if hasattr(target_node, 'ancestors'):
        ancestor_names = [ancestor.name for ancestor in target_node.ancestors]
        print(f"Ancestor names: {ancestor_names}")

    """
    Starting generating the explanation, according to the pdf it should contain a list of explanatory factors as defined below.
    The list should be obtained by traversing the tree in pre-order.
    """    
    agent_beliefs = beliefs.copy()
    for node in PreOrderIter(root):
        current_node_name = node.name
        current_node_type = None
        if hasattr(node, 'type'):
            current_node_type = node.type

        if current_node_name in chosen_trace:
            """ 
            (a) Pre-conditions of an action (denoted with a “P"). Requested format:
                ['P', action name,
                list of preconditions of the actions (including A) that were satisfied and that
                made the execution of action A that is being explained possible]
                Example: ['P', 'getOwnCard', ['ownCard']]
                Note: No "P" factor should be included in the list if an action has no preconditions.
            """
            if hasattr(node, 'pre') and node.name in chosen_trace and hasattr(node, 'type') and node.type in ['ACT']:
                # Add preconditions of cuurent action to the global preconditions list
                add_explanation(explanations, key='P', node_name=node.name, value=[node.pre.copy()])
            
            # Update agent beliefs given the execution of the current node
            if hasattr(node, 'post'):
                agent_beliefs.extend(node.post)

            # Handle OR nodes (b, c, d, e explanations [C, V, N, F])
            if current_node_type == 'OR':
                chosen_child = next(child for child in node.children if child.name in chosen_trace)
                chosen_child_name = chosen_child.name
                for child in node.children:
                    child_name = child.name
                    if child_name in chosen_trace:
                        """
                        (b) A condition of a choice (“C"). Requested format:
                            ['C', name of alternative that was chosen for an OR node,
                            list of preconditions of the alternative that were satisfied and that
                            made the choice possible]
                            Example: ['C', 'getKitchenCoffee', ['staffCardAvailable']]
                            Note: getKitchenCoffee is one of the alternatives of the getCoffee OR node
                        """
                        add_explanation(explanations, key='C', node_name=child_name, value=[chosen_child.pre.copy()])
                    else:
                        """
                        An explanation for each alternative not selected, either via a ”N” factor, a
                        ”V” factor, or a ”F” factor explanation, depending on the reason. Note:
                        if, for one alternative not selected, multiple reasons are true, only report
                        the first factor, considering the order above (i.e., a ”V” factor only if no
                        ”N” factor is relevant, and a ”F” factor only if no ”N” nor ”V” factors are
                        releant).
                        """

                        """
                        (d) A norm ("N"). Requested format:
                            ['N', name of an alternative of an OR node that was NOT chosen because
                            it violates (possibly through its children) a norm,
                            the norm that is violated]
                            Example: ['N', 'getShopCoffee', 'P(payShop)']
                        """
                        if hasattr(child, "violation") and child.violation:
                            norm_string = f"{norm['type']}({', '.join(norm['actions'])})"
                            add_explanation(explanations, key='N', node_name=child.name, value=[norm_string])
                            continue
                        """
                        (c) A value statement (“V"). Requested format:
                            ['V', name of an alternative that was chosen for an OR node,
                            list of costs for that alternative,
                            '>',
                            name of another alternative of an OR node that was NOT chosen,
                            list of costs for that alternative]
                            Example:
                            ['V', 'getKitchenCoffee', [5.0, 0.0, 3.0],
                            '>',
                            'getAnnOfficeCoffee', [2.0, 0.0, 6.0]]
                        """   
                        unsatisfied_preconditions = []
                        if hasattr(child, 'pre'):
                            unsatisfied_preconditions = [pre for pre in child.pre if pre not in agent_beliefs]             

                        if len(unsatisfied_preconditions) == 0:
                            chosen_child_cost = get_cost_of_node(valid_traces, valid_costs, chosen_child)                            
                            child_cost = get_cost_of_node(valid_traces, valid_costs, child)
                            child_cost_formatted = child_cost.tolist() if isinstance(child_cost, np.ndarray) else child_cost
                            chosen_child_cost_formatted = chosen_child_cost.tolist() if isinstance(chosen_child_cost, np.ndarray) else chosen_child_cost
                            add_explanation(explanations, key='V', 
                                            node_name=chosen_child_name, 
                                            value=[chosen_child_cost_formatted, '>',child_name, child_cost_formatted])
                            continue
                        

                        """
                        (e) A failed condition of a choice ("F"). Requested format:
                            ['F', name of an alternative of an OR node that was NOT chosen because
                            (some of) its pre-conditions were not satisfied,
                            list of preconditions of the alternative that were NOT
                            satisfied and made the choice not possible]
                            Example: ['F', 'getKitchenCoffee', ['staffCardAvailable']]
                        """                        
                        add_explanation(explanations, key='F', node_name=child_name, value=[unsatisfied_preconditions])
                        continue
            
            """ (g) A goal ("D"). Requested format:
                ['D', name of the goal]
                Example: ['D', 'getKitchenCoffee']
            """
            if current_node_type in ['SEQ', 'AND', 'OR'] and ancestor_names and len(ancestor_names) > 0 and current_node_name in ancestor_names:
                add_explanation(explanations, key='D', value=[current_node_name])

        # Check if the current node is the action to explain
        if current_node_name == action_to_explain:
            """
            (f) A link (“L"). Requested format:
                ['L', name of the node, '->', name of the linked node]
                Example: ['L', 'payShop', '->', 'getCoffeeShop']
                Note: a node a links to another node b if a's attribute "link" contains the
                name of b. Furthermore, if the linked node b also has a link to another node c,
                then the explanation should also include such a link (and all the links forming
                a chain starting from a) to the explanation, i.e., for each link in the chain an
                explanation in the requested format above should included in the list.
            """
            add_linked_node_explanations(explanations, node, root)
            # Stop the traversal if the action to explain is reached
            break

    

    """ (h) The user preference ("U"). Requested format:
        ['U' the pair given in input as user preference]
        Example: ['U', [['quality', 'price', 'time'], [1, 2, 0]]]
    """
    if preferences and len(preferences) == 2:
        add_explanation(explanations, key='U', value=[preferences])


    return explanations, chosen_trace

# output, selected_trace =  generate_explanations(json_tree, norm, goal, beliefs, preferences, action_to_explain)

# if __name__ == "__main__":
#     # norm = {'type': 'P', 'actions': ['gotoKitchen']}
#     # goal = ['haveCoffee']
#     # beliefs = ['staffCardAvailable', 'ownCard']
#     # preferences = [['quality', 'price', 'time'], [1, 2, 0]]
#     # action_to_explain = "getOthersCard"

#     norm = {"type": "P", "actions": ["payShop"]}
#     beliefs = ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney", "AnnInOffice"]
#     goal = ["haveCoffee"]
#     preferences = [["quality", "price", "time"], [1, 2, 0]]
#     action_to_explain = "getCoffeeKitchen"

#     current_dir = os.path.dirname(__file__)
#     # Read the JSON file into a dictionary
#     with open(f'{current_dir}/coffee.json', 'r') as file:
#         json_tree = json.load(file)
#     generate_explanations(json_tree, norm, goal, beliefs, preferences, action_to_explain, output_dir=current_dir)

#     if print_mode:
#         print("Exercise 4 is done running!")