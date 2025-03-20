"""
Generate naive baseline approch of if-else rules to generate naural language explanations
"""


def generate_naural_explentions(formal_explention, preferences):
    """
    Generate naive baseline approch of if-else rules to generate naural language explanations
    :param formal_explention: a single formal explentions (output of part1-4)
    :param preferences: user preferences
    :return: natural language explention
    """
    if formal_explention is None:
        print("No formal explention was given!")
        return None
    
    explanation_type = formal_explention[0]
    action = formal_explention[1]
    preferences_labels = preferences[0]
    preferences_values = preferences[1]
    preference_labels_formated = ', '.join(preferences_labels[preferences_values.index(0):])

    if explanation_type == 'C':  # Condition
        conditions = ', '.join(formal_explention[2])
        return f"Action '{action}' was performed because its preconditions: {conditions}, were all fulfilled."

    elif explanation_type == 'V':  # Value Comparison
        action1, values1, operator, action2, values2 = formal_explention[1:]
        for index, val1, val2 in enumerate(zip(values1, values2)):
            preference_label = preferences_labels[index]
            if val1 > val2:
                return f"Given the user's preferences to prioritize {preference_labels_formated} in that order, it is preferable to perform '{action1}' (with a {preference_label} value of {values1}) rather than '{action2}' (with a {preference_label} value of {values2})."
        
        return f"Both evaluated actions ({action1} and {action2}) have the same values for {preference_labels_formated}. So the agent chose to perform '{action1}'."

    elif explanation_type == 'N':  # Norm Violation
        return f"The action '{action}' is not allowed because it violates {formal_explention[2]}."

    elif explanation_type == 'P':  # Precondition
        preconditions = ', '.join(formal_explention[2])
        return f"To perform '{action}', you must first satisfy the following conditions: {preconditions}."

    elif explanation_type == 'D':  # Decision
        return f"The agent chose to perform '{action}'."

    elif explanation_type == 'U':  # Utility Function
        preferences = list(zip(formal_explention[1][0], formal_explention[1][1]))
        return f"The agent's preferences are: " + ', '.join([f"{p[0]} over {p[1]}" for p in preferences])

    return "Unknown explanation type."


def generate_naive_baseline(formal_explentions, preferences):
    """
    Generate naive baseline approch of if-else rules to generate naural language explanations
    :param formal_explentions: list of formal explentions (output of part1-4)
    :param preferences: user preferences

    :return: list of natural language explentions
    """
    natural_explentions = []
    # for explention in formal_explentions:
    for explention in formal_explentions:
        natural_explentions.append(generate_naural_explentions(explention, preferences))

    return natural_explentions

    

sample1 = [
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
preferences = [["quality", "price", "time"], [1, 2, 0]]
sample1_res = generate_naive_baseline(formal_explentions=sample1, preferences=preferences)

print(sample1_res)