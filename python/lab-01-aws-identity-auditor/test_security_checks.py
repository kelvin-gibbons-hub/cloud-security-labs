import unittest
from security_checks import classify_authorization

class TestAuthorizationClassifier(unittest.TestCase):

    
    def test_unexpected_success(self):
        result = classify_authorization(True)
        self.assertEqual(result, "FAIL")

    def test_access_denied(self):
        result = classify_authorization(False, "AccessDenied")
        self.assertEqual(result, "PASS")

    def test_access_denied_exception(self):
        result = classify_authorization(False, "AccessDeniedException")
        self.assertEqual(result, "PASS")

    def test_missing_entity(self):
        result = classify_authorization(False, "NoSuchEntity")
        self.assertEqual(result, "INCONCLUSIVE")

    def test_unexpected_error(self):
        result = classify_authorization(False, "Throttling")
        self.assertEqual(result, "ERROR")
