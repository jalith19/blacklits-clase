import unittest
from marshmallow import ValidationError

from src.models.blacklist import (
    BlacklistCreateSchema,
    BlacklistResponseSchema,
    BlacklistCheckResponseSchema,
    validate_uuid_format,
)


class BlacklistSchemaTestCase(unittest.TestCase):
    def setUp(self):
        self.create_schema = BlacklistCreateSchema()
        self.response_schema = BlacklistResponseSchema()
        self.check_schema = BlacklistCheckResponseSchema()

    def test_valid_create_data(self):
        data = {
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "Spam activity detected",
        }
        result = self.create_schema.load(data)
        self.assertEqual(result["email"], "user@example.com")
        self.assertEqual(result["app_uuid"], "123e4567-e89b-12d3-a456-426614174000")
        self.assertEqual(result["blocked_reason"], "Spam activity detected")

    def test_create_data_without_optional_reason(self):
        data = {
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        }
        result = self.create_schema.load(data)
        self.assertIsNone(result.get("blocked_reason"))

    def test_missing_email_fails(self):
        data = {
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        }
        with self.assertRaises(ValidationError):
            self.create_schema.load(data)

    def test_invalid_email_fails(self):
        data = {
            "email": "not-an-email",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
        }
        with self.assertRaises(ValidationError):
            self.create_schema.load(data)

    def test_missing_uuid_fails(self):
        data = {
            "email": "user@example.com",
        }
        with self.assertRaises(ValidationError):
            self.create_schema.load(data)

    def test_invalid_uuid_fails(self):
        data = {
            "email": "user@example.com",
            "app_uuid": "not-a-valid-uuid",
        }
        with self.assertRaises(ValidationError):
            self.create_schema.load(data)

    def test_blocked_reason_too_long_fails(self):
        data = {
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "x" * 256,
        }
        with self.assertRaises(ValidationError):
            self.create_schema.load(data)

    def test_blocked_reason_max_length_allowed(self):
        data = {
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": "x" * 255,
        }
        result = self.create_schema.load(data)
        self.assertEqual(len(result["blocked_reason"]), 255)

    def test_validate_uuid_function_valid(self):
        # valid UUID should not raise
        validate_uuid_format("123e4567-e89b-12d3-a456-426614174000")

    def test_validate_uuid_function_invalid(self):
        with self.assertRaises(ValidationError):
            validate_uuid_format("invalid-uuid")

    def test_validate_uuid_function_none(self):
        with self.assertRaises(ValidationError):
            validate_uuid_format(None)

    def test_response_schema(self):
        data = {
            "id": "abc-123",
            "email": "user@example.com",
            "app_uuid": "123e4567-e89b-12d3-a456-426614174000",
            "blocked_reason": None,
            "ip_address": "10.0.0.1",
            "created_at": "2024-01-01T00:00:00",
        }
        result = self.response_schema.load(data)
        self.assertEqual(result["email"], "user@example.com")

    def test_check_response_schema_blacklisted(self):
        data = {
            "is_blacklisted": True,
            "email": "user@example.com",
            "blocked_reason": "spam",
        }
        result = self.check_schema.load(data)
        self.assertTrue(result["is_blacklisted"])

    def test_check_response_schema_not_blacklisted(self):
        data = {
            "is_blacklisted": False,
            "email": "user@example.com",
            "blocked_reason": None,
        }
        result = self.check_schema.load(data)
        self.assertFalse(result["is_blacklisted"])


if __name__ == "__main__":
    unittest.main()
