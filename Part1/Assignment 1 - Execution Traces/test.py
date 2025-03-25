import unittest
from anytree.importer import DictImporter
from anytree import Node
import json
import os
from colorama import Fore, Style, init

from assigment1 import find_starting_node, generate_traces, main

class TestAssignment1(unittest.TestCase):

    def setUp(self):
        # Initialize colorama
        init(autoreset=True)
        
        # Load the JSON trees for testing
        self.current_dir = os.path.dirname(__file__)
        with open(f'{self.current_dir}/coffee.json', 'r') as file:
            self.coffee_tree = json.load(file)
        self.importer = DictImporter()

        # Define another tree for testing
        self.another_tree = {
            "name": "startNode",
            "type": "SEQ",
            "children": [
                {"name": "action1", "type": "ACT"},
                {"name": "action2", "type": "OR", "children": [
                    {"name": "action3", "type": "ACT"},
                    {"name": "action4", "type": "ACT"}
                ]}
            ]
        }

        # Define a more complex tree for testing
        self.complex_tree = {
            "name": "root",
            "type": "SEQ",
            "children": [
                {"name": "step1", "type": "ACT"},
                {"name": "step2", "type": "AND", "children": [
                    {"name": "substep1", "type": "ACT"},
                    {"name": "substep2", "type": "OR", "children": [
                        {"name": "option1", "type": "ACT"},
                        {"name": "option2", "type": "ACT"}
                    ]}
                ]},
                {"name": "step3", "type": "ACT"}
            ]
        }

    def test_find_starting_node(self):
        print(Fore.CYAN + "Running test_find_starting_node...")
        root = self.importer.import_(self.coffee_tree)
        starting_node_name = "getCoffee"
        starting_node = find_starting_node(root, starting_node_name)
        self.assertIsNotNone(starting_node, "Starting node not found")
        self.assertEqual(starting_node.name, starting_node_name, f"Expected starting node name to be {starting_node_name}")
        print(Fore.GREEN + "test_find_starting_node passed.")

    def test_generate_traces_coffee(self):
        print(Fore.CYAN + "Running test_generate_traces_coffee...")
        root = self.importer.import_(self.coffee_tree)
        starting_node_name = "getCoffee"
        starting_node = find_starting_node(root, starting_node_name)
        traces = generate_traces(starting_node)
        expected_traces = [
            ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen'],
            ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOthersCard', 'gotoKitchen', 'getCoffeeKitchen'],
            ['getCoffee', 'getAnnOfficeCoffee', 'gotoAnnOffice', 'getPod', 'getCoffeeAnnOffice'],
            ['getCoffee', 'getShopCoffee', 'gotoShop', 'payShop', 'getCoffeeShop']
        ]
        self.assertEqual(traces, expected_traces, "Traces do not match expected output for coffee tree starting at getCoffee")
        print(Fore.GREEN + "test_generate_traces_coffee passed.")

    def test_generate_traces_coffee_different_start(self):
        print(Fore.CYAN + "Running test_generate_traces_coffee_different_start...")
        root = self.importer.import_(self.coffee_tree)
        starting_node_name = "getKitchenCoffee"
        starting_node = find_starting_node(root, starting_node_name)
        traces = generate_traces(starting_node)
        expected_traces = [
            ['getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen'],
            ['getKitchenCoffee', 'getStaffCard', 'getOthersCard', 'gotoKitchen', 'getCoffeeKitchen']
        ]
        self.assertEqual(traces, expected_traces, "Traces do not match expected output for coffee tree starting at getKitchenCoffee")
        print(Fore.GREEN + "test_generate_traces_coffee_different_start passed.")

    def test_generate_traces_coffee_another_start(self):
        print(Fore.CYAN + "Running test_generate_traces_coffee_another_start...")
        root = self.importer.import_(self.coffee_tree)
        starting_node_name = "getAnnOfficeCoffee"
        starting_node = find_starting_node(root, starting_node_name)
        traces = generate_traces(starting_node)
        expected_traces = [
            ['getAnnOfficeCoffee', 'gotoAnnOffice', 'getPod', 'getCoffeeAnnOffice']
        ]
        self.assertEqual(traces, expected_traces, "Traces do not match expected output for coffee tree starting at getAnnOfficeCoffee")
        print(Fore.GREEN + "test_generate_traces_coffee_another_start passed.")

    def test_generate_traces_another_tree(self):
        print(Fore.CYAN + "Running test_generate_traces_another_tree...")
        root = self.importer.import_(self.another_tree)
        starting_node_name = "startNode"
        starting_node = find_starting_node(root, starting_node_name)
        traces = generate_traces(starting_node)
        expected_traces = [
            ['startNode', 'action1', 'action2', 'action3'],
            ['startNode', 'action1', 'action2', 'action4']
        ]
        self.assertEqual(traces, expected_traces, "Traces do not match expected output for another tree starting at startNode")
        print(Fore.GREEN + "test_generate_traces_another_tree passed.")

    def test_generate_traces_complex_tree(self):
        print(Fore.CYAN + "Running test_generate_traces_complex_tree...")
        root = self.importer.import_(self.complex_tree)
        starting_node_name = "root"
        starting_node = find_starting_node(root, starting_node_name)
        traces = generate_traces(starting_node)
        expected_traces = [
            ['root', 'step1', 'step2', 'substep1', 'substep2', 'option1', 'step3'],
            ['root', 'step1', 'step2', 'substep1', 'substep2', 'option2', 'step3']
        ]
        self.assertEqual(traces, expected_traces, "Traces do not match expected output for complex tree starting at root")
        print(Fore.GREEN + "test_generate_traces_complex_tree passed.")

    def test_main_coffee(self):
        print(Fore.CYAN + "Running test_main_coffee...")
        output_dir = self.current_dir
        traces = main(self.coffee_tree, starting_node_name="getCoffee", output_dir=output_dir)
        expected_traces = [
            ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen'],
            ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOthersCard', 'gotoKitchen', 'getCoffeeKitchen'],
            ['getCoffee', 'getAnnOfficeCoffee', 'gotoAnnOffice', 'getPod', 'getCoffeeAnnOffice'],
            ['getCoffee', 'getShopCoffee', 'gotoShop', 'payShop', 'getCoffeeShop']
        ]
        self.assertEqual(traces, expected_traces, "Main function traces do not match expected output for coffee tree starting at getCoffee")
        print(Fore.GREEN + "test_main_coffee passed.")

    def test_main_another_tree(self):
        print(Fore.CYAN + "Running test_main_another_tree...")
        output_dir = self.current_dir
        traces = main(self.another_tree, starting_node_name="startNode", output_dir=output_dir)
        expected_traces = [
            ['startNode', 'action1', 'action2', 'action3'],
            ['startNode', 'action1', 'action2', 'action4']
        ]
        self.assertEqual(traces, expected_traces, "Main function traces do not match expected output for another tree starting at startNode")
        print(Fore.GREEN + "test_main_another_tree passed.")

    def test_main_complex_tree(self):
        print(Fore.CYAN + "Running test_main_complex_tree...")
        output_dir = self.current_dir
        traces = main(self.complex_tree, starting_node_name="root", output_dir=output_dir)
        expected_traces = [
            ['root', 'step1', 'step2', 'substep1', 'substep2', 'option1', 'step3'],
            ['root', 'step1', 'step2', 'substep1', 'substep2', 'option2', 'step3']
        ]
        self.assertEqual(traces, expected_traces, "Main function traces do not match expected output for complex tree starting at root")
        print(Fore.GREEN + "test_main_complex_tree passed.")

if __name__ == '__main__':
    unittest.main()