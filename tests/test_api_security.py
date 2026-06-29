import unittest

from api.security import validate_bearer_token


class ApiSecurityTests(unittest.TestCase):
    def test_validate_bearer_token_rejects_missing_or_short_tokens(self):
        self.assertFalse(validate_bearer_token(None))
        self.assertFalse(validate_bearer_token(""))
        self.assertFalse(validate_bearer_token("Bearer x"))

    def test_validate_bearer_token_accepts_well_formed_bearer_tokens(self):
        self.assertTrue(validate_bearer_token("Bearer demo-token-123"))


if __name__ == "__main__":
    unittest.main()
