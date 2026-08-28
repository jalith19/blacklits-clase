import unittest

from src.models.errors import (
    BadRequestError,
    NotFoundError,
    UnauthorizedError,
    ConflictError,
)


class ErrorTestCase(unittest.TestCase):
    def test_bad_request_error_default(self):
        err = BadRequestError()
        self.assertEqual(err.message, "Bad request")
        self.assertIsNone(err.errors)

    def test_bad_request_error_with_args(self):
        err = BadRequestError(message="Invalid data", errors={"email": ["required"]})
        self.assertEqual(err.message, "Invalid data")
        self.assertEqual(err.errors, {"email": ["required"]})

    def test_not_found_error_default(self):
        err = NotFoundError()
        self.assertEqual(err.message, "Resource not found")

    def test_not_found_error_with_message(self):
        err = NotFoundError("Email not found")
        self.assertEqual(err.message, "Email not found")

    def test_unauthorized_error_default(self):
        err = UnauthorizedError()
        self.assertEqual(err.message, "Unauthorized")

    def test_unauthorized_error_with_message(self):
        err = UnauthorizedError("Token invalid")
        self.assertEqual(err.message, "Token invalid")

    def test_conflict_error_default(self):
        err = ConflictError()
        self.assertEqual(err.message, "Resource already exists")

    def test_conflict_error_with_message(self):
        err = ConflictError("Email already in blacklist")
        self.assertEqual(err.message, "Email already in blacklist")

    def test_exceptions_are_python_exceptions(self):
        self.assertTrue(issubclass(BadRequestError, Exception))
        self.assertTrue(issubclass(NotFoundError, Exception))
        self.assertTrue(issubclass(UnauthorizedError, Exception))
        self.assertTrue(issubclass(ConflictError, Exception))


if __name__ == "__main__":
    unittest.main()
