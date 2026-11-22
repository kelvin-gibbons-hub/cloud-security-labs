import json
from datetime import datetime


test_events1 = [
    {
        "request_fingerprint": "FP-001",
        "user_id": "alice",
        "decision": "BLOCK",
        "ts": "2026-02-05T04:00:00Z",
    },
    {
        "request_fingerprint": "FP-001",
        "user_id": "bob",
        "decision": "BAN",
        "ts": "INVALID",
    },
]

test_events2 = [
    {
        "request_fingerprint": "FP-001",
        "user_id": "alice",
        "decision": "BLOCK",
        "ts": "2026-02-05T04:00:00Z",
    },
    {
        "request_fingerprint": "FP-001",
        "user_id": None,
        "decision": "BLOCK",
        "ts": "2026-02-05T01:00:00Z",
    },
    {
        "request_fingerprint": "FP-001",
        "user_id": "bob",
        "decision": "BAN",
        "ts": "INVALID",
    },
]

def initialize_stats():
    return {
        "total_records": 0,
        "missing_fingerprint": 0,
        "missing_user": 0,
        "invalid_decision": 0,
        "invalid_timestamp": 0,
        "malformed_json": 0,
    }

def update_timestamps(record, timestamp):
	try:
		parsed = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
	except (AttributeError, ValueError):
		return False

	if parsed.tzinfo is None:
		return False

	if record["first_seen"] is None or parsed < record["first_seen"]:
		record["first_seen"] = parsed

	if record["last_seen"] is None or parsed > record["last_seen"]:
                record["last_seen"] = parsed	
	return True


def initialize_fingerprint(fingerprints, fingerprint):
	if fingerprint not in fingerprints:
		fingerprints[fingerprint] = {
	        "users": set(),
		"blocks": 0,
        	"events": 0,
		"first_seen": None,
		"last_seen": None,
		}

	return fingerprints[fingerprint]


def update_fingerprint(fingerprints, event):
	fingerprint = event.get("request_fingerprint")
	user_id = event.get("user_id")
	decision = event.get("decision")
	timestamp = event.get("ts")

	record = initialize_fingerprint(fingerprints, fingerprint)
	boolean_result = update_timestamps(record, timestamp)
	if isinstance(user_id, str) and user_id.strip():
		record["users"].add(user_id)

	record["events"] += 1

	if decision == "BLOCK":
		record["blocks"] += 1

	return boolean_result

def process_event(fingerprints, event, stats):
	stats["total_records"] += 1
	user_id = event.get("user_id")
        
	fingerprint = event.get("request_fingerprint")
	if (not isinstance(fingerprint, str) or not fingerprint.strip() or fingerprint.strip().lower() == "na"):
		stats["missing_fingerprint"] += 1

		return
	if not isinstance(user_id, str) or not user_id.strip():
		stats["missing_user"] += 1

	decision = event.get("decision")
	valid_decisions = {"SLOW", "ALLOW", "MONITOR", "BLOCK"}

	if decision not in valid_decisions:
		stats["invalid_decision"] += 1

	timestamp_valid = update_fingerprint(fingerprints, event)
	if timestamp_valid is False:
		stats["invalid_timestamp"] += 1

def find_repeat_offenders(fingerprints):
    matches = []

    for fingerprint, record in fingerprints.items():
        if len(record["users"]) >= 3 and record["blocks"] >= 5:
            new_record = {
            "fingerprint": fingerprint,
            "record": record
            }
            matches.append(new_record)
            

    return matches

def analyze_log(filename):
	fingerprints = {}
	stats = initialize_stats()

	with open(filename,"r", encoding="utf-8") as file:
		for line in file:
			if not line.strip():
				continue
			try:
				event = json.loads(line)
			except json.JSONDecodeError:
				stats["malformed_json"] += 1
				continue
			if not isinstance(event,dict):
				stats["malformed_json"] += 1
				continue

			process_event(fingerprints, event, stats)

	return fingerprints, stats


if __name__ == "__main__":
    fingerprints, stats = analyze_log("audit.log")
    matches = find_repeat_offenders(fingerprints)

    print("Total parsed records:", stats["total_records"])
    print("Validation statistics:", stats)
    print("Fingerprints analyzed:", len(fingerprints))
    print("Detection candidates:", len(matches))

    for match in matches:
        record = match["record"]
        print(
            "Fingerprint:", match["fingerprint"],
            "| Users:", len(record["users"]),
            "| BLOCK events:", record["blocks"],
            "| Total events:", record["events"],
            "| First:", record["first_seen"],
            "| Last:", record["last_seen"]
        )
