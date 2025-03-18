from anytree import NodeMixin, RenderTree, AnyNode
from anytree import RenderTree, AnyNode
from anytree.importer import DictImporter
import json

def build_tree(json_node, parent=None):
    # Build the entire tree
    attributes = {k: v for k, v in json_node.items() if k not in ['name', 'type', 'children']}
    node = AnyNode(name=json_node['name'], type=json_node['type'], violation=False, parent=parent, **attributes)
    
    for child in json_node.get('children', []):
        build_tree(child, node)
    
    return node

def annotate_tree(node, norm):
    """
    Annotates the tree by marking nodes that violate the given norm.
    - If the norm is of type 'P' (prohibited), a node violates it if its name is in norm['actions'].
    - If the norm is of type 'O' (obligatory), a node violates it if it is an action but not in norm['actions'].
    """
    # Based on norm gives P or O.
    if norm['type'] == 'P':
        node.violation = node.name in norm['actions']
    elif norm['type'] == 'O':
        node.violation = node.name not in norm['actions'] and node.type == 'ACT'

    # Parent check - Checks if child node has violated the norms.
    if node.type in ['SEQ', 'AND', 'OR']:
        node.violation = any(child.violation for child in node.children)

    # Recursive function to run on the whole tree.
    for child in node.children:
        annotate_tree(child, norm) 

root = build_tree(json_tree)

# Executed twice because first time all the children are marked as violated, second iteration the parents of the children are also makred as violated.
annotate_tree(root, norm)
annotate_tree(root, norm)

# remove_violate_parents(root)
output = RenderTree(root)
print(output)