"""
User domain services.
Domain services contain business logic that doesn't naturally fit in entities.
"""

from app.domain.user.value_objects import Email
from app.domain.user.repositories import UserRepository
from app.core.exceptions import UserAlreadyExistsError


class UserDomainService:
    """
    Domain service for User-related business logic.
    """

    def __init__(self, user_repository: UserRepository):
        """
        Initialize domain service.

        Args:
            user_repository: User repository for data access
        """
        self.user_repository = user_repository

    def validate_unique_email(self, email: Email) -> None:
        """
        Validate that email is unique (not already registered).

        Args:
            email: Email address to validate

        Raises:
            UserAlreadyExistsError: If email is already registered
        """
        if self.user_repository.exists_by_email(email):
            raise UserAlreadyExistsError(
                f"User with email {email.value} already exists"
            )

    def can_delete_user(self, user_id: str) -> bool:
        """
        Check if a user can be deleted.
        Business rules for deletion can be added here.

        Args:
            user_id: User's unique identifier

        Returns:
            True if user can be deleted, False otherwise
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            return False

        # Business rules for deletion
        # For now, any user can be deleted
        # In the future, might prevent deletion if user has active generations, etc.
        return True
