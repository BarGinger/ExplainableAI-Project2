"""
Generate naive baseline approach of if-else rules to generate natural language explanations
"""

def handle_condition_explanation(action, formal_explention):
    conditions = ', '.join(formal_explention[2])
    return f"The agent was able to perform the action '{action}' as all its preconditions ({conditions}) were successfully met."

def handle_value_comparison_explanation(action1, values1, operator, action2, values2, preferences_labels, preferences_values, preference_labels_formatted):
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

def handle_norm_violation_explanation(action, formal_explention):
    norm = formal_explention[2]
    norm_type = norm[0]
    norm_action = norm[2:-1]
    
    if norm_type == "P":  # Prohibition Norm
        if norm_action == action:
            return f"The action '{action}' is not allowed because it violates the prohibition norm, which states that this action cannot be executed."
        
        return f"The action '{action}' is not allowed because it leads to the execution of a prohibited action. The prohibition norm specifies that the following action must not be performed: {norm_action}."
    
    elif norm_type == "O":  # Obligation Norm
        return f"The action '{action}' is not allowed because it violates the obligation norm, which specifies that only the following action(s) are permitted: {norm_action}."

def handle_precondition_explanation(action, formal_explention):
    preconditions = formal_explention[2]
    if len(preconditions) > 1:
        preconditions_formatted = ', '.join(preconditions[:-1]) + ', and ' + preconditions[-1]
        return f"The agent could not perform '{action}' because the obligatory preconditions: {preconditions_formatted} were not met."
    else:
        preconditions_formatted = preconditions[0]
        return f"The agent could not perform '{action}' because the obligatory precondition: {preconditions_formatted} was not met."

def handle_decision_explanation(action):
    return f"The agent chose to perform '{action}' as it is a necessary step to achieve the goal action."

def handle_link_explanation(action, formal_explention):
    linked_action = formal_explention[3]
    return f"The action '{action}' is linked to the action '{linked_action}', and as such, it was executed as a necessary step to achieve the goal action."

def handle_utility_function_explanation(preferences):
    preferences_labels = preferences[0]
    preferences_values = preferences[1]
    # Sort preferences_labels according to preferences_values
    preference_labels_sorted = [preferences_labels[i] for i in preferences_values]
    if len(preference_labels_sorted) > 1:
        preference_labels_formatted = ', '.join(preference_labels_sorted[:-1]) + ', and ' + preference_labels_sorted[-1]
    else:
        preference_labels_formatted = preference_labels_sorted[0]
    return f"The agent's preferences, in descending order of importance, are: {preference_labels_formatted}."

def handle_failure_explanation(action, formal_explention):
    """
    (e) A failed condition of a choice ("F"). Requested format:
        ['F', name of an alternative of an OR node that was NOT chosen because
        (some of) its pre-conditions were not satisfied,
        list of preconditions of the alternative that were NOT
        satisfied and made the choice not possible]
        Example: ['F', 'getKitchenCoffee', ['staffCardAvailable']]
    """     
    alternative = formal_explention[1]
    preconditions = formal_explention[2]
    if len(preconditions) > 1:
        preconditions_labels_formatted = ', '.join(preconditions[:-1]) + ', and ' + preconditions[-1]
    else:
        preconditions_labels_formatted = preconditions[0]
    
    return f"The agent executed '{action}' because the preconditions for the alternative action '{alternative}', which are {preconditions_labels_formatted}, were not met."

def generate_natural_explentions(formal_explention, preferences):
    """
    Generate naive baseline approach of if-else rules to generate natural language explanations
    :param formal_explention: a single formal explentions (output of part1-4)
    :param preferences: user preferences
    :return: natural language explention
    """
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
        return handle_condition_explanation(action, formal_explention)
    elif explanation_type == 'V':  # Value Comparison
        action1, values1, operator, action2, values2 = formal_explention[1:]
        return handle_value_comparison_explanation(action1, values1, operator, action2, values2, preferences_labels, preferences_values, preference_labels_formatted)
    elif explanation_type == 'N':  # Norm Violation
        return handle_norm_violation_explanation(action, formal_explention)
    elif explanation_type == 'P':  # Precondition
        return handle_precondition_explanation(action, formal_explention)
    elif explanation_type == 'D':  # Decision
        return handle_decision_explanation(action)
    elif explanation_type == 'L':  # Link
        return handle_link_explanation(action, formal_explention)
    elif explanation_type == 'U':  # Utility Function
        return handle_utility_function_explanation(preferences)
    elif explanation_type == 'F':
        return handle_failure_explanation(action, formal_explention)
    
    return "Unknown explanation type."

def generate_naive_baseline(formal_explentions, chosen_trace, norm, goal, beliefs, preferences, action_to_explain):
    """
    Generate naive baseline approach of if-else rules to generate natural language explanations
    
    Parameters:
    formal_explentions (list): list of formal explentions (output of part1-4)
    chosen_trace (list): chosen trace
    norm (dict): The norm
    goal (list): The goal of the agent: a set of beliefs (strings) of the agent that must be true at the end of the execution of the trace.
    beliefs (list): A set of strings representing the initial beliefs of the agents.
    preferences (list): A pair describing the preference of the end-user.
    action_to_explain (string): The name of the action to explain.

    :return: list of natural language explentions
    """
    natural_explentions = []
    if chosen_trace is not None and len(chosen_trace) > 0:
       chosen_trace_formatted = ', '.join(chosen_trace)

    if formal_explentions is None or len(formal_explentions) == 0:
        if chosen_trace is not None:
            return [f"The target action to explain '{action_to_explain}' was not  exectued in the chosen trace ({chosen_trace_formatted})."]
        
        return ["No valid execution path was found given the current restrictions."]

    for explention in formal_explentions:
        natural_explentions.append(generate_natural_explentions(explention, preferences))

    return natural_explentions

# sample1 = [['C', 'getAnnOfficeCoffee', ['AnnInOffice']], ['N', 'getKitchenCoffee', 'P(gotoKitchen)'], ['V', 'getAnnOfficeCoffee', [2, 0, 6], '>', 'getShopCoffee', [0, 3, 9]], ['P', 'gotoAnnOffice', ['AnnInOffice']], ['L', 'getPod', '->', 'getCoffeeAnnOffice'], ['D', 'getAnnOfficeCoffee'], ['D', 'getCoffee'], ['U', [['quality', 'price', 'time'], [2, 0, 1]]]]
# preferences = [["quality", "price", "time"], [1, 2, 0]]
# sample1_res = generate_naive_baseline(formal_explentions=sample1, preferences=preferences)

# print('\n '.join(sample1_res))