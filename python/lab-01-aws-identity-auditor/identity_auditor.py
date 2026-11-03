import boto3
from botocore.exceptions import ClientError
	

def display_identity(identity):
	print("UserId:", identity["UserId"])
	print("Account:", identity["Account"])
	print("Role Arn:", identity["Arn"])

					
def inspect_role():
    session = boto3.Session(profile_name="auditor-live")
    iam = session.client("iam")

    response = iam.get_role(RoleName="lab-lambda-readonly")
    role = response["Role"]

    print("\n=== IAM Role Inspection ===")
    print("Role Name:", role["RoleName"])
    print("Role ARN:", role["Arn"])
    print("Created:", role["CreateDate"])


def test_live_access_denied():
    session = boto3.Session(profile_name="auditor-live")
    iam = session.client("iam")

    print("\n=== Least-Privilege Test ===")

    try:
        iam.get_role(RoleName="SecurityLabAdminRole")
        print("UNEXPECTED: Restricted role inspection succeeded.")

    except ClientError as error:
        error_code = error.response["Error"]["Code"]


    if error_code in ("AccessDenied", "AccessDeniedException"):
    	print("PASS: Unauthorized role inspection denied.")
    elif error_code == "NoSuchEntity":
    	print("INCONCLUSIVE: Target IAM role not found.")
    else:
    	print("ERROR: Unexpected AWS error:", error_code)



def identify_principal():
	session = boto3.Session(profile_name="auditor-live")
	sts = session.client("sts")

	print("AWS Identity Auditor")
	print("Identity inspection initialized.")
	
	identity = sts.get_caller_identity()
	
	display_identity(identity)	


def main():
    print("\n=== AWS Identity Auditor v1 ===")
    identify_principal()
    inspect_role()
    test_live_access_denied()
    print("Audit completed.")

if __name__ == "__main__":
    main()

