import boto3
import json
from botocore.exceptions import ClientError
from security_checks import classify_authorization
from error_handling import classify_aws_exception	

def run_audit_check(check_name, check_function):
    try:
        return check_function()

    except Exception as error:
        finding = classify_aws_exception(error)

        finding["check"] = check_name
        finding["principal"] = None

        return finding


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
        finding["result"] = classify_authorization(True)

    except ClientError as error:
        error_code = error.response["Error"]["Code"]

        finding["error_code"] = error_code
        finding["result"] = classify_authorization(
            False, error_code
        )

    return finding



def identify_principal():
	session = boto3.Session(profile_name="auditor-live")
	sts = session.client("sts")

	print("AWS Identity Auditor")
	print("Identity inspection initialized.")
	
	identity = sts.get_caller_identity()
	
	display_identity(identity)	




def main():
    print("\n=== AWS Identity Auditor v5 ===")
    
    #identify_principal()
       
    authorized = run_audit_check(
    "authorized_role_inspection",
    inspect_role
    )

    unauthorized = run_audit_check(
    "unauthorized_role_inspection",
    test_live_access_denied
    )
    
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

