import unittest
import json
import os
from assigment3 import main
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
        norm = {'type': 'P', 'actions': ['payShop']}
        goal = ['haveCoffee']
        beliefs = ['haveMoney']
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]
        expected_output = [] # ['getCoffee', 'getShopCoffee', 'gotoShop', 'payShop', 'getCoffeeShop']

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 1 passed")
        except AssertionError:
            print(Fore.RED + "Test case 1 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

    def test_case_2(self):
        norm = {'type': 'P', 'actions': ['payShop']}
        goal = ['haveCoffee']
        beliefs = []
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]
        expected_output = []

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 2 passed")
        except AssertionError:
            print(Fore.RED + "Test case 2 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise



    def test_case_3(self):
        norm = {'type': 'P', 'actions': ['gotoAnnOffice']}
        goal = ['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard']
        preferences = [['quality', 'price', 'time'], [1, 2, 0]]
        expected_output = ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen']

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 3 passed")
        except AssertionError:
            print(Fore.RED + "Test case 3 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

    def test_case_4(self):
        norm = {'type': 'O', 'actions': ['gotoShop', 'payShop', 'getCoffeeShop']}
        goal =	['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard']
        preferences = [['quality', 'price', 'time'], [1, 2, 0]]

        expected_output = []
        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 4 passed")
        except AssertionError:
            print(Fore.RED + "Test case 4 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

    def test_case_5(self):
        norm = {'type': 'P', 'actions': ['gotoAnnOffice']}
        goal = ['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard', 'colleagueAvailable', 'haveMoney', 'AnnInOffice']
        preferences = [['quality', 'price', 'time'], [1, 2, 0]]

        expected_output = ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen']

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 5 passed")
        except AssertionError:
            print(Fore.RED + "Test case 5 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise
    
    def test_case_6(self):
        norm = {}
        goal = ['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard', 'colleagueAvailable', 'haveMoney', 'AnnInOffice']
        preferences = [['quality', 'price', 'time'], [1, 2, 0]]

        expected_output = ['getCoffee', 'getKitchenCoffee', 'getStaffCard', 'getOwnCard', 'gotoKitchen', 'getCoffeeKitchen']

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 6 passed")
        except AssertionError:
            print(Fore.RED + "Test case 6 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

    def test_case_7(self):
        norm = {'type': 'O', 'actions': ['gotoShop', 'payShop', 'getCoffeeShop']}
        goal = ['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard', 'colleagueAvailable', 'haveMoney', 'AnnInOffice']
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]

        expected_output = ['getCoffee', 'getShopCoffee', 'gotoShop', 'payShop', 'getCoffeeShop']

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 7 passed")
        except AssertionError:
            print(Fore.RED + "Test case 7 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

    def test_case_8(self):
        norm = {'type': 'P', 'actions': ['gotoKitchen']}
        goal = ['haveCoffee']
        beliefs = ['staffCardAvailable', 'ownCard']
        preferences = [['quality', 'price', 'time'], [2, 0, 1]]

        expected_output = []

        output = main(self.json_tree, norm, goal, beliefs, preferences)
        try:
            self.assertEqual(output, expected_output)
            print(Fore.GREEN + "Test case 8 passed")
        except AssertionError:
            print(Fore.RED + "Test case 8 failed")
            print(Fore.RED + f"Expected: {expected_output}")
            print(Fore.RED + f"Got: {output}")
            raise

if __name__ == '__main__':
    unittest.main()