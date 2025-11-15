"""
User repository interface.
Defines the contract for user persistence without implementation details.
"""

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user.entities import User
from app.domain.user.value_objects import Email


class UserRepository(ABC):
    """
    Repository interface for User aggregate.
    Infrastructure layer will implement this interface.
    """

    @abstractmethod
    def create(self, user: User) -> User:
        """
        Create a new user.

        Args:
            user: User entity to persist

        Returns:
            Created user entity

        Raises:
            UserAlreadyExistsError: If user with email already exists
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Get user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_email(self, email: Email) -> Optional[User]:
        """
        Get user by email address.

        Args:
            email: User's email address

        Returns:
            User entity if found, None otherwise
        """
        pass

    @abstractmethod
    def update(self, user: User) -> User:
        """
        Update an existing user.

        Args:
            user: User entity with updated values

        Returns:
            Updated user entity

        Raises:
            UserNotFoundError: If user doesn't exist
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        """
        Delete a user by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            True if deleted, False if user not found
        """
        pass

    @abstractmethod
    def exists_by_email(self, email: Email) -> bool:
        """
        Check if user with email exists.

        Args:
            email: Email address to check

        Returns:
            True if user exists, False otherwise
        """
        pass
