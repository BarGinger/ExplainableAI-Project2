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

        output = generate_explanations(self.json_tree, norm, goal, beliefs, preferences, action_to_explain)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 1 passed")
        except AssertionError:
            print(Fore.RED + "Test case 1 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise
    

if __name__ == '__main__':
    unittest.main()