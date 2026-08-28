import unittest
from unittest.mock import Mock

from src.utils.validation import validate_uuid, get_client_ip
from src.models.errors import BadRequestError


class RequestStub:
    def __init__(self, headers=None, remote_addr=None):
        self.headers = headers or {}
        self.remote_addr = remote_addr


class ValidationTestCase(unittest.TestCase):
    def test_validate_uuid_valid(self):
        self.assertTrue(validate_uuid("123e4567-e89b-12d3-a456-426614174000"))

    def test_validate_uuid_invalid_raises(self):
        with self.assertRaises(BadRequestError):
            validate_uuid("not-a-uuid")

    def test_get_client_ip_with_forwarded_for(self):
        request = RequestStub(
            headers={"X-Forwarded-For": "203.0.113.5, 10.0.0.1"},
            remote_addr="10.0.0.1",
        )
        self.assertEqual(get_client_ip(request), "203.0.113.5")

    def test_get_client_ip_without_forwarded_for(self):
        request = RequestStub(headers={}, remote_addr="192.168.1.100")
        self.assertEqual(get_client_ip(request), "192.168.1.100")

    def test_get_client_ip_defaults_to_unknown(self):
        request = RequestStub(headers={}, remote_addr=None)
        self.assertEqual(get_client_ip(request), "unknown")

    def test_get_client_ip_forwarded_has_single_ip(self):
        request = RequestStub(
            headers={"X-Forwarded-For": "203.0.113.5"},
            remote_addr="10.0.0.1",
        )
        self.assertEqual(get_client_ip(request), "203.0.113.5")


if __name__ == "__main__":
    unittest.main()
