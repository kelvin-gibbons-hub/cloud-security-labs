import boto3
import json
from botocore.exceptions import ClientError
	

def display_identity(identity):
	print("UserId:", identity["UserId"])
	print("Account:", identity["Account"])
	print("Role Arn:", identity["Arn"])

					
def inspect_role():
    session = boto3.Session(profile_name="auditor-live")
    iam = session.client("iam")
    sts = session.client("sts")

    response = iam.get_role(RoleName="lab-lambda-readonly")
    role = response["Role"]
    caller_id = sts.get_caller_identity()

    finding = {
    'check': 'authorized_role_inspection',
    'result': 'PASS',
    'principal': caller_id["Arn"],
    'error_code': None
    }
    return finding



def test_live_access_denied():
    session = boto3.Session(profile_name="auditor-live")
    iam = session.client("iam")
    sts = session.client("sts")

    user = sts.get_caller_identity()

    finding = {
        "check": "unauthorized_role_inspection",
        "result": "ERROR",
        "principal": user["Arn"],
        "error_code": None
    }

    try:
        iam.get_role(RoleName="SecurityLabAdminRole")
        finding["result"] = "FAIL"

    except ClientError as error:
        error_code = error.response["Error"]["Code"]
        finding["error_code"] = error_code

        if error_code in ("AccessDenied", "AccessDeniedException"):
            finding["result"] = "PASS"
        elif error_code == "NoSuchEntity":
            finding["result"] = "INCONCLUSIVE"
        else:
            finding["result"] = "ERROR"

    return finding


def identify_principal():
	session = boto3.Session(profile_name="auditor-live")
	sts = session.client("sts")

	print("AWS Identity Auditor")
	print("Identity inspection initialized.")
	
	identity = sts.get_caller_identity()
	
	display_identity(identity)	


def main():
    print("\n=== AWS Identity Auditor v3 ===")
    
    identify_principal()
    
    authorized = inspect_role()
    unauthorized = test_live_access_denied()
    
    report = {
        "auditor_version": "3.0",
        "profile": "auditor-live",
        "checks": [authorized, unauthorized]
    }
    with open("audit_results.json", "w") as file:
        json.dump(report, file, indent=4)

    print("Authorized check:", authorized)
    print("Unauthorized check:", unauthorized)    
    print("\nAudit completed.")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()

