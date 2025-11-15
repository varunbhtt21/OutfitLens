"""
Authentication application service.
Handles user registration, login, and authentication use cases.
"""

from datetime import timedelta

from app.domain.user.entities import User
from app.domain.user.value_objects import Email, Password
from app.domain.user.repositories import UserRepository
from app.domain.user.services import UserDomainService
from app.application.dtos.user_dtos import CreateUserDTO, UserDTO
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.exceptions import (
    InvalidCredentialsError,
    UserNotFoundError,
    UserInactiveError,
)


class AuthService:
    """
    Application service for authentication use cases.
    Orchestrates domain logic and infrastructure.
    """

    def __init__(
        self,
        user_repository: UserRepository,
        user_domain_service: UserDomainService,
    ):
        """
        Initialize authentication service.

        Args:
            user_repository: User repository for data access
            user_domain_service: User domain service for business logic
        """
        self.user_repository = user_repository
        self.user_domain_service = user_domain_service

    def register_user(self, dto: CreateUserDTO) -> UserDTO:
        """
        Register a new user.

        Args:
            dto: User registration data

        Returns:
            UserDTO with created user information

        Raises:
            UserAlreadyExistsError: If email is already registered
            InvalidEmailError: If email format is invalid
            InvalidPasswordError: If password doesn't meet requirements
        """
        # Create value objects (validation happens here)
        email = Email(dto.email)
        password = Password(dto.password)

        # Check if email is unique (domain service)
        self.user_domain_service.validate_unique_email(email)

        # Hash password
        hashed_password = hash_password(password.value)

        # Create user entity
        user = User.create(
            email=email,
            hashed_password=hashed_password,
            full_name=dto.full_name,
        )

        # Persist user
        created_user = self.user_repository.create(user)

        # Convert to DTO and return
        return self._to_dto(created_user)

    def login(self, email: str, password: str) -> dict[str, str]:
        """
        Authenticate user and generate tokens.

        Args:
            email: User's email address
            password: User's password

        Returns:
            Dictionary with access_token and refresh_token

        Raises:
            InvalidCredentialsError: If email or password is incorrect
            UserInactiveError: If user account is inactive
        """
        # Get user by email
        email_vo = Email(email)
        user = self.user_repository.get_by_email(email_vo)

        if not user:
            raise InvalidCredentialsError("Invalid email or password")

        # Verify password
        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Invalid email or password")

        # Check if user can login
        if not user.can_login():
            raise UserInactiveError("User account is inactive")

        # Generate tokens
        access_token = create_access_token(data={"sub": user.id})
        refresh_token = create_refresh_token(data={"sub": user.id})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    def refresh_token(self, refresh_token: str) -> dict[str, str]:
        """
        Generate new access token from refresh token.

        Args:
            refresh_token: Valid refresh token

        Returns:
            Dictionary with new access_token

        Raises:
            InvalidTokenError: If refresh token is invalid
            UserNotFoundError: If user no longer exists
        """
        from app.core.security import decode_token, verify_token_type

        # Decode and validate refresh token
        payload = decode_token(refresh_token)

        if not verify_token_type(payload, "refresh"):
            from app.core.exceptions import InvalidTokenError
            raise InvalidTokenError("Token is not a refresh token")

        user_id = payload.get("sub")
        if not user_id:
            from app.core.exceptions import InvalidTokenError
            raise InvalidTokenError("Token does not contain user ID")

        # Verify user still exists
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")

        # Generate new access token
        access_token = create_access_token(data={"sub": user.id})

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    def verify_email(self, user_id: str) -> UserDTO:
        """
        Mark user's email as verified.

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

        # Mark email as verified (domain logic)
        user.verify_email()

        # Persist changes
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
