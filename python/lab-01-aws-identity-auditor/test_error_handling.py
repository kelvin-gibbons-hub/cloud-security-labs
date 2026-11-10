import unittest

from botocore.exceptions import (
    NoCredentialsError,
    CredentialRetrievalError,
    EndpointConnectionError,
    ClientError,
)

from error_handling import classify_aws_exception


class TestAWSExceptionHandling(unittest.TestCase):

    def test_no_credentials(self):
        error = NoCredentialsError()
        finding = classify_aws_exception(error)

        self.assertEqual(finding["result"], "ERROR")
        self.assertEqual(finding["error_code"], "NoCredentials")
        self.assertFalse(finding["retryable"])

    def test_credentials_retreival(self):
        error = CredentialRetrievalError(
        provider="test-provider",
        error_msg="Simulated credential expiration"
        )
        finding = classify_aws_exception(error)

        self.assertEqual(finding["result"], "ERROR")
        self.assertEqual(finding["error_code"], "CredentialRetrievalError")
        self.assertFalse(finding["retryable"])

    def test_endpoint_connection(self):
        error = EndpointConnectionError(
        endpoint_url="https://sts.us-east-1.amazonaws.com"
        )
        finding = classify_aws_exception(error)

        self.assertEqual(finding["result"], "ERROR")
        self.assertEqual(finding["error_code"], "EndpointConnectionError")
        self.assertTrue(finding["retryable"])

    def test_expired_token(self):
        error = ClientError(
        {
        "Error": {
            "Code": "ExpiredToken",
            "Message": "Simulated expired token"
            }
        },
        "GetCallerIdentity"
        )
        finding = classify_aws_exception(error)

        self.assertEqual(finding["result"], "ERROR")
        self.assertEqual(finding["error_code"], "ExpiredToken")
        self.assertFalse(finding["retryable"])

    def test_unexpected_error(self):
        error = ValueError("Simulated unexpected failure")
        finding = classify_aws_exception(error)

        self.assertEqual(finding["result"], "ERROR")
        self.assertEqual(finding["error_code"], "UnexpectedError")
        self.assertFalse(finding["retryable"])	
