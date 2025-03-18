import unittest
from anytree.importer import DictImporter
from anytree import Node, RenderTree
import json
import os

from assigment2 import build_tree, annotate_tree, export_tree_to_png, main

class TestAssignment2(unittest.TestCase):

    def setUp(self):
        # Load the JSON trees for testing
        self.current_dir = os.path.dirname(__file__)
        with open(f'{self.current_dir}/coffee.json', 'r') as file:
            self.coffee_tree = json.load(file)
        self.importer = DictImporter()

    def test_annotate_tree_prohibited(self):
        print("Running test_annotate_tree_prohibited...")
        norm = {'type': 'P', 'actions': ['payShop']}
        root = build_tree(self.coffee_tree)
        annotate_tree(root, norm)

        # Check the violation status of nodes
        self.assertFalse(root.violation, "Root node should not be in violation")
        self.assertTrue(root.children[2].violation, "Node 'getShopCoffee' should be in violation")
        self.assertTrue(root.children[2].children[1].violation, "Node 'payShop' should be in violation")
        print("test_annotate_tree_prohibited passed.")

    def test_annotate_tree_obligatory(self):
        print("Running test_annotate_tree_obligatory...")
        norm = {'type': 'O', 'actions': ['getOwnCard', 'gotoKitchen', 'getCoffeeKitchen']}
        root = build_tree(self.coffee_tree)
        annotate_tree(root, norm)

        # Check the violation status of nodes
        self.assertFalse(root.violation, "Root node should not be in violation")
        self.assertFalse(root.children[0].violation, "Node 'getKitchenCoffee' should not be in violation")
        self.assertFalse(root.children[0].children[0].violation, "Node 'getStaffCard' should not be in violation")
        self.assertFalse(root.children[0].children[0].children[0].violation, "Node 'getOwnCard' should not be in violation")
        self.assertFalse(root.children[0].children[1].violation, "Node 'gotoKitchen' should not be in violation")
        self.assertFalse(root.children[0].children[2].violation, "Node 'getCoffeeKitchen' should not be in violation")
        print("test_annotate_tree_obligatory passed.")

    def test_main_function(self):
        print("Running test_main_function...")
        norm = {'type': 'P', 'actions': ['payShop']}
        output_dir = self.current_dir
        output = main(self.coffee_tree, norm=norm, output_dir=output_dir)

        # Check the violation status of nodes
        root = output.node
        self.assertFalse(root.violation, "Root node should not be in violation")
        self.assertTrue(root.children[2].violation, "Node 'getShopCoffee' should be in violation")
        self.assertTrue(root.children[2].children[1].violation, "Node 'payShop' should be in violation")
        print("test_main_function passed.")

if __name__ == '__main__':
    unittest.main()