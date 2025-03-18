"""
HW2.1. Practice - Assignment 1 - Execution Traces

Write an algorithm that determines all the possible behaviors (execution traces) that an agent could exhibit, based on its goal tree.

The setup code gives the following variables:
Name	Type	Description
json_tree	json object	The goal tree
starting_node_name	string	The name of the node to start traversing the tree from (e.g., the name of the root node of the tree).

Your code snippet should define the following variables:

Name	Type	Description
output	list	A list of lists, where each inner list represents an execution trace starting from the starting node.

Instructions:
A file coffee.json is provided as input for the exercise and pre-loaded for you in the variable json_tree.
For this variant of the exercise, the starting node name is "getStaffCard".
After saving and grading this variant, press the New Variant button to try a different variant.

Write an algorithm that enumerates all potential traces by traversing the goal tree according to its semantics starting from a given input node. For instance OR goal nodes can be satisfied by any one of their children, SEQ goal nodes are satisfied by executing all their children sequentially. Note: For the purposes of this project, treat AND and SEQ nodes as identical.
An execution trace is composed of the nodes from the starting input node to one (or more, in the case of SEQ or AND goals) leaf node(s).
As a final output of the algorithm, for this assignment, for each trace, please represent each node only via its name.

"""
 # Import nessary packages
from anytree import Node, RenderTree
from anytree.importer import DictImporter
from anytree.exporter import DotExporter
from anytree import Node, RenderTree, AsciiStyle, PreOrderIter
from anytree.search import find
from itertools import product

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
    if node:
        print(f"Node found: {node.name}")
    else:
        print("Node not found")

    return node

def generate_traces(node):
    """Recursively generates all possible traces from the given node."""
    if not hasattr(node, 'children') or not node.children:
        return [[node.name]]  # Leaf node (ACT), end of a trace
    
    traces = []
    
    if node.type == "OR":
        # OR node: Select one child at a time
        for child in node.children:
            child_traces = generate_traces(child)
            for trace in child_traces:
                traces.append([node.name] + trace)
    
    elif node.type == "SEQ":
        # SEQ/AND node: Concatenate traces of all children in order
        child_traces = [generate_traces(child) for child in node.children]
        for combination in product(*child_traces):
            traces.append([node.name] + [step for trace in combination for step in trace])
    
    return traces


def main(json_tree, starting_node_name, output_dir=""):
    """
    Parameters:
    json_tree (json object): The goal tree 
    starting_node_name (string): The name of the node to start traversing the tree from
    output_dir (string): The directory to save the output image

    return:
    output (list): A list of lists, where each inner list represents an execution trace starting from the starting node.
    """

    # Print input
    # print(f" this is the JSON input: {json_tree}")

    # Import dic input into anytree structure using anytree lib
    importer = DictImporter()
    root = importer.import_(json_tree)

    # Visualize the tree graphically as an image
    DotExporter(root).to_picture(f"{output_dir}/tree.png")

    # Find the goal node
    starting_node = find_starting_node(root, starting_node_name)

    print("Traversing the tree to generate traces")
    traces = generate_traces(starting_node)

    print("Traces generated:")
    for trace in traces:
        print(trace)

    # Pretty print the traces
    print("\nPretty Printed Traces:")
    for trace in traces:
        print(" -> ".join(trace))

    # Export traces to a text file
    with open(f"{output_dir}/traces.txt", "w") as file:
        for trace in traces:
            file.write(str(trace) + "\n")

    # Export pretty printed traces to a text file
    with open(f"{output_dir}/pretty_traces.txt", "w") as file:
        for trace in traces:
            file.write(" -> ".join(trace) + "\n")

    return traces

if __name__ == "__main__":
    import json
    import os
    
    current_dir = os.path.dirname(__file__)
    # Read the JSON file into a dictionary
    with open(f'{current_dir}/coffee.json', 'r') as file:
        json_tree = json.load(file)
    main(json_tree, starting_node_name="getCoffee", output_dir=current_dir)

    print("Exercise 1 is done running")