
def evaluate_policy(policy, action, resource):
    statement = policy["Statement"]
    allow_found = False
    for item in statement:
        action_matches = action in item["Action"]

        resource_matches = (
        resource in item["Resource"]
        or "*" in item["Resource"]
        )	

        matches = action_matches and resource_matches
        effect = item["Effect"]

        if matches and effect == "Deny":
            return "DENY"
        
        if matches and effect == "Allow":
            allow_found = True
    
    if allow_found:
        return "ALLOW"

    else:
        return "IMPLICIT_DENY"
            
