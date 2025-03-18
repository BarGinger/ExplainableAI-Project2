from anytree.importer import DictImporter
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


def main(json_tree, starting_node_name):
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
    
    
    return traces
    
output = main(json_tree, starting_node_name)