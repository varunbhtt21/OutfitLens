"""
User domain entities.
These represent the core business concepts in the User domain.
"""

from datetime import datetime
from app.domain.shared.base import AggregateRoot
from app.domain.user.value_objects import Email
from app.domain.shared.events import UserRegisteredEvent, UserVerifiedEvent


class User(AggregateRoot):
    """
    User aggregate root.
    Represents a user account with authentication and profile information.
    """

    def __init__(
        self,
        email: Email,
        hashed_password: str,
        full_name: str | None = None,
        is_active: bool = True,
        is_verified: bool = False,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
    ):
        """
        Create a User entity.

        Args:
            email: User's email address
            hashed_password: Hashed password (should be hashed before creating entity)
            full_name: User's full name
            is_active: Whether the user account is active
            is_verified: Whether the user's email is verified
            id: Unique identifier (generates if not provided)
            created_at: Creation timestamp (sets to now if not provided)
            updated_at: Last update timestamp (sets to now if not provided)
        """
        super().__init__(id)

        self.email = email
        self.hashed_password = hashed_password
        self.full_name = full_name
        self.is_active = is_active
        self.is_verified = is_verified

        if created_at:
            self.created_at = created_at
        if updated_at:
            self.updated_at = updated_at

    @staticmethod
    def create(
        email: Email, hashed_password: str, full_name: str | None = None
    ) -> "User":
        """
        Factory method to create a new user.

        Args:
            email: User's email address
            hashed_password: Already hashed password
            full_name: User's full name

        Returns:
            New User instance with UserRegisteredEvent added
        """
        user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            is_active=True,
            is_verified=False,
        )

        # Add domain event
        user.add_domain_event(UserRegisteredEvent.create(user.id, email.value))

        return user

    def verify_email(self) -> None:
        """
        Mark the user's email as verified.
        Raises a UserVerifiedEvent.
        """
        if not self.is_verified:
            self.is_verified = True
            self.update_timestamp()
            self.add_domain_event(UserVerifiedEvent.create(self.id))

    def activate(self) -> None:
        """Activate the user account."""
        if not self.is_active:
            self.is_active = True
            self.update_timestamp()

    def deactivate(self) -> None:
        """Deactivate the user account."""
        if self.is_active:
            self.is_active = False
            self.update_timestamp()

    def update_profile(self, full_name: str | None = None) -> None:
        """
        Update user profile information.

        Args:
            full_name: New full name (if provided)
        """
        if full_name is not None:
            self.full_name = full_name
            self.update_timestamp()

    def update_password(self, new_hashed_password: str) -> None:
        """
        Update user's password.

        Args:
            new_hashed_password: New hashed password
        """
        self.hashed_password = new_hashed_password
        self.update_timestamp()

    def can_login(self) -> bool:
        """
        Check if user can log in.

        Returns:
            True if user is active, False otherwise
        """
        return self.is_active

    def __repr__(self) -> str:
        """String representation of user."""
        return f"User(id={self.id!r}, email={self.email.value!r}, is_active={self.is_active})"
