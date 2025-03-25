"""
HW1.1. Exercise 0 - Get Acquainted with Anytree

Please do the following exercise to getting acquainted with Anytree and with PairieLearn.

The exercise is not evaluated for the final Project grade.

Objective: Import and visualize the provided example tree for the coffee scenario.

The setup code gives the following variables:

Name	Type	Description
json_tree	json object	The tree
Your code snippet should define the following variables:

Name	Type	Description
output	string	The printed tree
Instructions:
A file coffee.json is provided as input for the exercise and already loaded for you in variable json_tree.

Import the example tree into an anytree structure
Visualize the tree textually, i.e., printed as a structured representation using the RenderTree function.
(Optional but recommended) Visualize the tree graphically, i.e., as an image. Note: 
This should not be done via Prairielearn, but on your own machine and Python environment.
This step is recommended so that you set up your own Python environment. This will be necessary for Part 2
 of the Project.
Tip: take this opportunity to look at and experiment with the documentation of anytree
 (https://anytree.readthedocs.io/en/latest/index.html), and the different functions that it offers.

Tip 2: If your answer is incorrect, check the message output of the score below. 
For homework and practice exercises, it will provide the correct answer.

"""


def main(json_tree, output_dir=""):
    # Import nessary packages
    from anytree.importer import DictImporter
    from anytree import RenderTree
    from anytree.exporter import DotExporter


    # Print input
    print(f" this is the JSON input: {json_tree}")

    # Import dic input into anytree structure using anytree lib
    importer = DictImporter()
    root = importer.import_(json_tree)

    # Create output - printed structured representation using the RenderTree function
    output = RenderTree(root)
    print(output)

    # Visualize the tree graphically as an image
    DotExporter(root).to_picture(f"{output_dir}/tree.png")

    return output

if __name__ == "__main__":
    import json
    import os

    current_dir = os.path.dirname(__file__)
    # Read the JSON file into a dictionary
    with open(f'{current_dir}/coffee.json', 'r') as file:
        json_tree = json.load(file)
    main(json_tree, output_dir=current_dir)

    print("Exercise 0 is done running")