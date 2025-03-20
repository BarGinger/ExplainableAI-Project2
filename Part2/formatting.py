def format_formal(explanation):
    "Convert formal explanation into a structured text format"

    explanation_type = explanation[0]
    action = explanation[1]

    #condition
    if explanation_type == "C": 
        condition = ',' .join(explanation[2])
        return f"Condition (C): The action '{action}' was executed because {condition}."
    
   #Value
    elif explanation_type == "V":
        action1, values1, operator, action2, values2 = explanation[1:]
        return f"Disclaimer: [quality, price, time],  smaller values means lower 'cost' -> better . e.g. quality = 2 < quality = 0\nValues (V): The action '{action1}' was executed because the {values1} of '{action1}' {operator} the {values2} of '{action2}'."  
    
    #Norm violation
    elif explanation_type == "N":
        norm = explanation[2]
        return f"Norm violation (N): The action '{action}' violates  {norm}."
    #precondition
    elif explanation_type == "P":
        precondition = ',' .join(explanation[2])
        return f"Precondition (P): The action '{action}' was executed because {precondition}."
    #decision
    elif explanation_type == "D":
        decision = explanation[2]
        return f"Decision (D): The action '{action}' was executed because {decision}."
    
    #utility
    elif explanation_type == "U":
        attributes = explanation[1][0]
        preference = explanation[1][1]
        formatted_preference =',' .join([f"{attributes[i]}={preference[i]}" for i in range(len(attributes))])
        return f"Utility (U): The action '{action}' was executed because it has the highest utility based on the preferences: {formatted_preference}."
    
    return "Invalid explanation type."

print(format_formal((['C', 'getKitchenCoffee', ['staffCardAvailable']])))
print(format_formal(['V', 'getOwnCard', [0,0,0], '>', 'getOthersCard', [0,0,2]]))
# "V: getOwnCard [0,0,0] > getOthersCard [0,0,2]"