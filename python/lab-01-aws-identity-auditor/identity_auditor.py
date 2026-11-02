import boto3
from botocore.exceptions import ClientError


def simulate_access_denied():
    error_response = {
        "Error": {
            "Code": "AccessDenied",
            "Message": "Not authorized to perform iam:ListUsers"
        }
    }

    raise ClientError(error_response, "ListUsers")

def test_error_handling():
	try:
		simulate_access_denied()
	except ClientError as error:
		error_code = error.response["Error"]["Code"]
		print("Permission denied:", error_code)	
	

def display_identity(identity):
	print("UserId:", identity["UserId"])
	print("Account:", identity["Account"])
	print("Role Arn:", identity["Arn"])

					


def identify_principal():
	session = boto3.Session()
	sts = session.client("sts")

	print("AWS Identity Auditor")
	print("Identity inspection initialized.")
	
	identity = {
        "UserId": "AROEXAMPLE:lab-session",
        "Account": "123456789012",
        "Arn": "arn:aws:sts::123456789012:assumed-role/SecurityLabOperatorRole/lab-session"
    }
	
	display_identity(identity)	



def main():
    print("=== AWS Identity Auditor v1 ===")
    identify_principal()
    test_error_handling()
    print("Audit completed.")

if __name__ == "__main__":
    main()
