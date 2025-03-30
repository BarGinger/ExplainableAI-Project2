# Import nessary packages
from anytree.exporter import DotExporter
from anytree.search import find
from itertools import product
from anytree import RenderTree, AnyNode
from anytree import RenderTree, AnyNode
import os

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

def generate_traces(node):
    """
    Recursively generates all possible traces from the given node.

    Parameters:
    node (Node): The current node in the tree.

    Returns:
    list: A list of all possible traces from the given node.
    """
    if not hasattr(node, 'children') or not node.children:
        return [[node.name]]  # Leaf node (ACT), end of a trace
    
    traces = []
    
    if node.type == "OR":
        # OR node: Select one child at a time
        for child in node.children:
            child_traces = generate_traces(child)
            for trace in child_traces:
                traces.append([node.name] + trace)
    
    elif node.type == "SEQ" or node.type == "AND":
        # SEQ/AND node: Concatenate traces of all children in order
        child_traces = [generate_traces(child) for child in node.children]
        for combination in product(*child_traces):
            traces.append([node.name] + [step for trace in combination for step in trace])
    
    return traces


def build_tree(json_node, parent=None):
    """
    Recursively builds a tree structure from the given JSON node.
    Parameters:
    json_node (dict): The JSON node to build the tree from
    parent (Node): The parent node in the tree

    Returns:
    Node: The root node of the tree
    """
    # Build the entire tree
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
    """
    DotExporter(root, 
                nodeattrfunc=lambda node: f'label="{node.name}\nViolation: {node.violation}"'
               ).to_picture(output_file)

def main(json_tree, norm, output_dir=""):
    """
    Parameters:
    json_tree (json object): The goal tree 
    norm (dict): The norm
    output_dir (string): The directory to save the output image

    return:
    output (anytree.render.RenderTree): The annotated tree, rendered using the function RenderTree of anytree.
    """

    # Import dic input into anytree structure using anytree lib
    root = build_tree(json_tree)
    annotate_tree(root, norm)

    # remove_violate_parents(root)
    output = RenderTree(root)
    if print_mode:
        print(output)
        output_file = os.path.join(output_dir, "annotated_tree.png")
        export_tree_to_png(root, output_file)
    return output
    
output = main(json_tree, norm)