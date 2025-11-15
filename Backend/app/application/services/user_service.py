"""
User management application service.
Handles user profile and account management use cases.
"""

from app.domain.user.entities import User
from app.domain.user.value_objects import Password
from app.domain.user.repositories import UserRepository
from app.domain.user.services import UserDomainService
from app.application.dtos.user_dtos import UserDTO, UpdateUserDTO, ChangePasswordDTO
from app.core.security import hash_password, verify_password
from app.core.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    AuthorizationError,
)


class UserService:
    """
    Application service for user management use cases.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        user_domain_service: UserDomainService,
    ):
        """
        Initialize user service.

        Args:
            user_repository: User repository for data access
            user_domain_service: User domain service for business logic
        """
        self.user_repository = user_repository
        self.user_domain_service = user_domain_service

    def get_user_profile(self, user_id: str) -> UserDTO:
        """
        Get user profile by ID.

        Args:
            user_id: User's unique identifier

        Returns:
            UserDTO with user information

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        return self._to_dto(user)

    def update_user_profile(self, user_id: str, dto: UpdateUserDTO) -> UserDTO:
        """
        Update user profile information.

        Args:
            user_id: User's unique identifier
            dto: Update data

        Returns:
            Updated UserDTO

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        # Update profile (domain logic)
        user.update_profile(full_name=dto.full_name)

        # Persist changes
        updated_user = self.user_repository.update(user)

        return self._to_dto(updated_user)

    def change_password(self, user_id: str, dto: ChangePasswordDTO) -> bool:
        """
        Change user's password.

        Args:
            user_id: User's unique identifier
            dto: Password change data

        Returns:
            True if password was changed successfully

        Raises:
            UserNotFoundError: If user doesn't exist
            InvalidCredentialsError: If old password is incorrect
            InvalidPasswordError: If new password doesn't meet requirements
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        # Verify old password
        if not verify_password(dto.old_password, user.hashed_password):
            raise InvalidCredentialsError("Current password is incorrect")

        # Validate new password
        new_password = Password(dto.new_password)

        # Hash new password
        new_hashed_password = hash_password(new_password.value)

        # Update password (domain logic)
        user.update_password(new_hashed_password)

        # Persist changes
        self.user_repository.update(user)

        return True

    def delete_user_account(self, user_id: str, requesting_user_id: str) -> bool:
        """
        Delete user account.

        Args:
            user_id: User's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            True if account was deleted

        Raises:
            UserNotFoundError: If user doesn't exist
            AuthorizationError: If requesting user is not authorized
        """
        # Verify user can only delete their own account
        if user_id != requesting_user_id:
            raise AuthorizationError("You can only delete your own account")

        # Check if user can be deleted (domain service)
        if not self.user_domain_service.can_delete_user(user_id):
            raise AuthorizationError("User cannot be deleted at this time")

        # Delete user
        deleted = self.user_repository.delete(user_id)

        if not deleted:
            raise UserNotFoundError(f"User not found: {user_id}")

        return True

    def activate_user(self, user_id: str) -> UserDTO:
        """
        Activate a user account.

        Args:
            user_id: User's unique identifier

        Returns:
            Updated UserDTO

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        user.activate()
        updated_user = self.user_repository.update(user)

        return self._to_dto(updated_user)

    def deactivate_user(self, user_id: str) -> UserDTO:
        """
        Deactivate a user account.

        Args:
            user_id: User's unique identifier

        Returns:
            Updated UserDTO

        Raises:
            UserNotFoundError: If user doesn't exist
        """
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        user.deactivate()
        updated_user = self.user_repository.update(user)

        return self._to_dto(updated_user)

    # Helper methods

    def _to_dto(self, user: User) -> UserDTO:
        """Convert User entity to UserDTO."""
        return UserDTO(
            id=user.id,
            email=user.email.value,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
