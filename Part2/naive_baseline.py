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
    # Sort preferences_labels according to preferences_values
    preference_labels_sorted = [preferences_labels[i] for i in preferences_values]
    if len(preference_labels_sorted) > 1:
        preference_labels_formatted = ', '.join(preference_labels_sorted[:-1]) + ', and ' + preference_labels_sorted[-1]
    else:
        preference_labels_formatted = preference_labels_sorted[0]

    
    if explanation_type == 'C':  # Condition
        """
        (b) A condition of a choice (“C"). Requested format:
            ['C', name of alternative that was chosen for an OR node,
            list of preconditions of the alternative that were satisfied and that
            made the choice possible]
            Example: ['C', 'getKitchenCoffee', ['staffCardAvailable']]
            Note: getKitchenCoffee is one of the alternatives of the getCoffee OR node
        """
        conditions = ', '.join(formal_explention[2])
        return f"The agent was able to perform the action '{action}' as all its preconditions ({conditions}) were successfully met."

    elif explanation_type == 'V':  # Value Comparison
        """
            (c) A value statement (“V"). Requested format:
                ['V', name of an alternative that was chosen for an OR node,
                list of costs for that alternative,
                '>',
                name of another alternative of an OR node that was NOT chosen,
                list of costs for that alternative]
                Example:
                ['V', 'getKitchenCoffee', [5.0, 0.0, 3.0],
                '>',
                'getAnnOfficeCoffee', [2.0, 0.0, 6.0]]
        """
        action1, values1, operator, action2, values2 = formal_explention[1:]
        value1_formatted = ', '.join([f"{label}: {value}" for label, value in zip(preferences_labels, values1)])
        value2_formatted = ', '.join([f"{label}: {value}" for label, value in zip(preferences_labels, values2)])
        

        if values1 == values2:
            return f"Both actions have the same values for all factors ({value1_formatted}), so the agent randomly chose '{action1}' over '{action2}."
        
        explanation = f"The agent chose '{action1}' over '{action2}' based on the user's preferences to prioritize {preference_labels_formatted}"

        # Compare the values succinctly
        explanation += f" and given that '{action1}' has these values: " + value1_formatted
        explanation += f", while '{action2}' has: " + value2_formatted

        # Find the decisive factor
        for index in preferences_values:
            preference_label = preferences_labels[index]
            value1 = values1[index]
            value2 = values2[index]

            if value1 != value2:
                explanation += f". The decisive factor was the {preference_label}, as '{action2}' had a higher value of {value2} compared to '{action1}' with {value1}. Lower values are more desirable, so '{action1}' was chosen."
                break

        # If all values are equal
        if not any(value1 != value2 for value1, value2 in zip(values1, values2)):
            explanation += f". Since all factors were equally matched, the agent randomly chose the first action ({action1})."

        return explanation        
        
    elif explanation_type == 'N':  # Norm Violation
        """
        (d) A norm ("N"). Requested format:
            ['N', name of an alternative of an OR node that was NOT chosen because
            it violates (possibly through its children) a norm,
            the norm that is violated]
            Example: ['N', 'getShopCoffee', 'P(payShop)']
        """
        norm = formal_explention[2]
        norm_type = norm[0]
        norm_action = norm[2:-1]
        
        if norm_type == "P":  # Prohibition Norm
            if norm_action == action:
                return f"The action '{action}' is not allowed because it violates the prohibition norm, which states that this action cannot be executed."
            
            return f"The action '{action}' is not allowed because it leads to the execution of a prohibited action. The prohibition norm specifies that the following action must not be performed: {norm_action}."
        
        elif norm_type == "O":  # Obligation Norm
            return f"The action '{action}' is not allowed because it violates the obligation norm, which specifies that only the following action(s) are permitted: {norm_action}."
    
    elif explanation_type == 'P':  # Precondition
        """ 
        (a) Pre-conditions of an action (denoted with a “P"). Requested format:
            ['P', action name,
            list of preconditions of the actions (including A) that were satisfied and that
            made the execution of action A that is being explained possible]
            Example: ['P', 'getOwnCard', ['ownCard']]
            Note: No "P" factor should be included in the list if an action has no preconditions.
        """
        preconditions = formal_explention[2]
        if len(preconditions) > 1:
            preconditions_formatted = ', '.join(preconditions[:-1]) + ', and ' + preconditions[-1]
            return f"The agent could not perform '{action}' because the obligatory preconditions: {preconditions_formatted} were not met."
        else:
            preconditions_formatted = preconditions[0]
            return f"The agent could not perform '{action}' because the obligatory precondition: {preconditions_formatted} was not met."

        
    elif explanation_type == 'D':  # Decision
        """ (g) A goal ("D"). Requested format:
                ['D', name of the goal]
                Example: ['D', 'getKitchenCoffee']
            """
        return f"The agent chose to perform '{action}' as it is a necessary step to achieve the goal action."
    elif explanation_type == 'L':  # Link
        """
            (f) A link (“L"). Requested format:
                ['L', name of the node, '->', name of the linked node]
                Example: ['L', 'payShop', '->', 'getCoffeeShop']
                Note: a node a links to another node b if a's attribute "link" contains the
                name of b. Furthermore, if the linked node b also has a link to another node c,
                then the explanation should also include such a link (and all the links forming
                a chain starting from a) to the explanation, i.e., for each link in the chain an
                explanation in the requested format above should included in the list.
            """
        linked_action = formal_explention[3]
        return f"The action '{action}' is linked to the action '{linked_action}' as a necessary step to achieve the goal action."
    elif explanation_type == 'U':  # Utility Function
        """ (h) The user preference ("U"). Requested format:
        ['U' the pair given in input as user preference]
        Example: ['U', [['quality', 'price', 'time'], [1, 2, 0]]]
        """
        preferences_labels = preferences[0]
        preferences_values = preferences[1]
        # Sort preferences_labels according to preferences_values
        preference_labels_sorted = [preferences_labels[i] for i in preferences_values]
        if len(preference_labels_sorted) > 1:
            preference_labels_formatted = ', '.join(preference_labels_sorted[:-1]) + ', and ' + preference_labels_sorted[-1]
        else:
            preference_labels_formatted = preference_labels_sorted[0]
        return f"The agent's preferences, in descending order of importance, are: {preference_labels_formatted}."

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

    

sample1 = [['C', 'getAnnOfficeCoffee', ['AnnInOffice']], ['N', 'getKitchenCoffee', 'P(gotoKitchen)'], ['V', 'getAnnOfficeCoffee', [2, 0, 6], '>', 'getShopCoffee', [0, 3, 9]], ['P', 'gotoAnnOffice', ['AnnInOffice']], ['L', 'getPod', '->', 'getCoffeeAnnOffice'], ['D', 'getAnnOfficeCoffee'], ['D', 'getCoffee'], ['U', [['quality', 'price', 'time'], [2, 0, 1]]]]
preferences = [["quality", "price", "time"], [1, 2, 0]]
sample1_res = generate_naive_baseline(formal_explentions=sample1, preferences=preferences)

print('\n '.join(sample1_res))