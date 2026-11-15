import json

def sort_findings(findings):
	by_time = sorted(findings, key=lambda finding: finding["timestamp"])

	return by_time
	

def extract_finding(event):
	params = event.get("requestParameters", {}) or {}
	
	finding = {
	"timestamp": event.get("eventTime", "UNKNOWN"),
	"action": event.get("eventName", "UNKNOWN"),
	"principal": (event.get("userIdentity") or {}).get("arn", "UNKNOWN"),
	"target": params.get("roleName") or params.get("name") or "UNKNOWN",
	"outcome": "ERROR"
	}
	
	if event.get("errorCode") is None:
		finding["outcome"] = "SUCCESS"
	elif event.get("errorCode") == "AccessDenied":
		finding["outcome"] = "DENIED"
	return finding


def load_events(filename):
	with open(filename, "r", encoding = "utf-8") as file:
		data = json.load(file)

	return data["Records"]


def detect_high_risk_events(events):
	
	high_risk_actions = {
    	"AttachRolePolicy",
	"PutRolePolicy",
    	"StopLogging",
	}

	match = []
	for event in events:
		action = event.get("eventName", "UNKNOWN")
		if action in high_risk_actions:
			match.append(event)

	return match	
			
		
if __name__ == "__main__":
    events = load_events("sample_events.json")
    matches = detect_high_risk_events(events)

    findings = [extract_finding(event) for event in matches]
    ordered = sort_findings(findings)
    
    for finding in ordered:
        print(
            finding["timestamp"],
            finding["action"],
            finding["principal"],
            finding["target"],
            finding["outcome"]
        )