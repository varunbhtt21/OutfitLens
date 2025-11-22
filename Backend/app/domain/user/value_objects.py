"""
Value objects for the User domain.
Value objects are immutable and represent concepts with no identity.
"""

import re
from app.domain.shared.base import ValueObject
from app.core.exceptions import InvalidEmailError, InvalidPasswordError


class Email(ValueObject):
    """
    Email value object with validation.
    Ensures email addresses are valid.
    """

    # Email regex pattern (basic validation)
    EMAIL_PATTERN = re.compile(
        r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    )

    def __init__(self, value: str):
        """
        Create an Email value object.

        Args:
            value: Email address string

        Raises:
            InvalidEmailError: If email format is invalid
        """
        if not value:
            raise InvalidEmailError("Email cannot be empty")

        value = value.lower().strip()

        if not self.EMAIL_PATTERN.match(value):
            raise InvalidEmailError(f"Invalid email format: {value}")

        if len(value) > 255:
            raise InvalidEmailError("Email must be 255 characters or less")

        self.value = value

    def __str__(self) -> str:
        """String representation of email."""
        return self.value


class Password(ValueObject):
    """
    Password value object with strength validation.
    Ensures passwords meet security requirements.
    """

    MIN_LENGTH = 8
    MAX_LENGTH = 128

    def __init__(self, value: str, skip_validation: bool = False):
        """
        Create a Password value object.

        Args:
            value: Password string
            skip_validation: Skip validation (for already hashed passwords)

        Raises:
            InvalidPasswordError: If password doesn't meet requirements
        """
        if not skip_validation:
            self._validate(value)

        self.value = value

    def _validate(self, password: str) -> None:
        """
        Validate password strength.

        Args:
            password: Password to validate

        Raises:
            InvalidPasswordError: If password doesn't meet requirements
        """
        if not password:
            raise InvalidPasswordError("Password cannot be empty")

        if len(password) < self.MIN_LENGTH:
            raise InvalidPasswordError(
                f"Password must be at least {self.MIN_LENGTH} characters long"
            )

        if len(password) > self.MAX_LENGTH:
            raise InvalidPasswordError(
                f"Password must be {self.MAX_LENGTH} characters or less"
            )

        # Relaxed validation - just check length
        # Users can use any combination of characters as long as it's 8+ chars

    def __str__(self) -> str:
        """String representation (hidden for security)."""
        return "********"

    def __repr__(self) -> str:
        """Representation (hidden for security)."""
        return "Password(********)"
