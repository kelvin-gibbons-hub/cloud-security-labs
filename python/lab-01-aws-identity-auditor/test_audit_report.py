import json

with open("audit_results.json", "r") as file:
    report = json.load(file)

assert report["auditor_version"] == "3.0"
assert len(report["checks"]) == 2

authorized = report["checks"][0]
unauthorized = report["checks"][1]

assert authorized["check"] == "authorized_role_inspection"
assert authorized["result"] == "PASS"

assert unauthorized["check"] == "unauthorized_role_inspection"
assert unauthorized["result"] == "PASS"

assert unauthorized["error_code"] in (
    "AccessDenied",
    "AccessDeniedException"
)

print("PASS: JSON audit report validation completed.")
