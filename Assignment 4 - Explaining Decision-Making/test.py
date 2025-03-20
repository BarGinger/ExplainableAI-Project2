import unittest
import json
import os
from assigment4 import generate_explanations
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class TestAssignment3(unittest.TestCase):

    def setUp(self):
        # Load the JSON tree for testing
        self.current_dir = os.path.dirname(__file__)
        with open(f'{self.current_dir}/coffee.json', 'r') as file:
            self.json_tree = json.load(file)

    def compare_outputs(self, output, expected_output, test_index):
        """
        Helper function to compare the output with the expected output and print detailed differences.

        Parameters:
        output (list): The actual output from the function
        expected_output (list): The expected output
        test_index (int): The index of the test case
        """
        def normalize(item):
            if isinstance(item, list):
                return tuple(normalize(sub_item) for sub_item in item)
            return item

        output_set = set(normalize(item) for item in output)
        expected_output_set = set(normalize(item) for item in expected_output)

        if output_set == expected_output_set:
            print(Fore.GREEN + f"Test case {test_index} passed")
        else:
            print(Fore.RED + f"Test case {test_index} failed")
            print(Fore.RED + f"Expected: {expected_output} \n")
            print(Fore.RED + f"Got: {output} \n")

            # Find elements in expected_output that are not in output
            missing_from_output = expected_output_set - output_set
            if missing_from_output:
                print(Fore.RED + "Missing from output:")
                for item in missing_from_output:
                    print(Fore.RED + f"  {item}")

            # Find elements in output that are not in expected_output
            extra_in_output = output_set - expected_output_set
            if extra_in_output:
                print(Fore.RED + "Extra in output:")
                for item in extra_in_output:
                    print(Fore.RED + f"  {item}")

            raise AssertionError("Output does not match expected output")

    def test_case_1(self):
        norm = {"type": "P", "actions": ["payShop"]}
        beliefs = ["staffCardAvailable", "ownCard", "colleagueAvailable", "haveMoney", "AnnInOffice"]
        goal = ["haveCoffee"]
        preferences = [["quality", "price", "time"], [1, 2, 0]]
        action_to_explain = "getCoffeeKitchen"
        expected_output = [
            ['C', 'getKitchenCoffee', ['staffCardAvailable']],
            ['V', 'getKitchenCoffee', [5.0, 0.0, 3.0], '>', 'getAnnOfficeCoffee', [2.0, 0.0, 6.0]],
            ['N', 'getShopCoffee', 'P(payShop)'],
            ['C', 'getOwnCard', ['ownCard']],
            ['V', 'getOwnCard', [0.0, 0.0, 0.0], '>', 'getOthersCard', [0.0, 0.0, 2.0]],
            ['P', 'getOwnCard', ['ownCard']],
            ['P', 'getCoffeeKitchen', ['haveCard', 'atKitchen']],
            ['D', 'getKitchenCoffee'],
            ['D', 'getCoffee'],
            ['U', [['quality', 'price', 'time'], [1, 2, 0]]]
        ]

        output, selected_trace = generate_explanations(self.json_tree, norm, goal, beliefs, preferences, action_to_explain)
        self.compare_outputs(output, expected_output, 1)

    def test_case_2(self):
        norm = {'type': 'P', 'actions': ['gotoAnnOffice']}
        goal = ['haveCoffee']
        beliefs = ['haveMoney']
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]
        action_to_explain = "payShop"
        expected_output = [['C', 'getShopCoffee', ['haveMoney']], ['F', 'getKitchenCoffee', ['staffCardAvailable']], ['N', 'getAnnOfficeCoffee', 'P(gotoAnnOffice)'], ['P', 'payShop', ['haveMoney']], ['L', 'payShop', '->', 'getCoffeeShop'], ['D', 'getShopCoffee'], ['D', 'getCoffee'], ['U', [['quality', 'price', 'time'], [2, 0, 1]]]]

        output, selected_trace = generate_explanations(self.json_tree, norm, goal, beliefs, preferences, action_to_explain)
        self.compare_outputs(output, expected_output, 2)

    def test_case_3(self):
        norm = {'type': 'O', 'actions': ['gotoShop', 'payShop', 'getCoffeeShop']}
        goal =	['haveCoffee']
        beliefs	= ['staffCardAvailable', 'ownCard']
        preferences	= [['quality', 'price', 'time'], [2, 0, 1]]
        action_to_explain =	"getOthersCard"
        expected_output = []

        output, selected_trace = generate_explanations(self.json_tree, norm, goal, beliefs, preferences, action_to_explain)
        self.compare_outputs(output, expected_output, 3)

    def test_case_4(self):
        norm = {'type': 'P', 'actions': ['gotoKitchen']}
        goal = ['haveCoffee']
        beliefs =['staffCardAvailable', 'ownCard', 'colleagueAvailable', 'haveMoney', 'AnnInOffice']
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]
        action_to_explain = "getCoffeeAnnOffice"
        expected_output = [['C', 'getAnnOfficeCoffee', ['AnnInOffice']], ['N', 'getKitchenCoffee', 'P(gotoKitchen)'], ['V', 'getAnnOfficeCoffee', [2, 0, 6], '>', 'getShopCoffee', [0, 3, 9]], ['P', 'gotoAnnOffice', ['AnnInOffice']], ['P', 'getCoffeeAnnOffice', ['havePod', 'atAnnOffice']], ['D', 'getAnnOfficeCoffee'], ['D', 'getCoffee'], ['U', [['quality', 'price', 'time'], [2, 0, 1]]]]

        output, selected_trace = generate_explanations(self.json_tree, norm, goal, beliefs, preferences, action_to_explain)
        self.compare_outputs(output, expected_output, 4)

if __name__ == '__main__':
    unittest.main()