from botocore.exceptions import (
    NoCredentialsError,
    CredentialRetrievalError,
    EndpointConnectionError,
    ClientError,
)

def classify_aws_exception(error):
    
    finding = {
    "result": "ERROR",
    "error_code": "UnexpectedError",
    "message": "Unexpected audit failure",
    "retryable": False
    }

    if isinstance(error, NoCredentialsError):
        finding["error_code"] = "NoCredentials"
        finding["message"] = "AWS credentials unavailable"
       
    elif isinstance(error, CredentialRetrievalError):
        finding["error_code"] = "CredentialRetrievalError"
        finding["message"] = "AWS could not retrieve credentials"
        

    elif isinstance(error, EndpointConnectionError):
        finding["error_code"] = "EndpointConnectionError"
        finding["message"] = "AWS endpoint connection failed"
        finding["retryable"] = True

    elif isinstance(error, ClientError):
        error_code = error.response["Error"]["Code"]
        finding["error_code"] = error_code
        finding["message"] = "AWS service request failed"
      
    return finding
