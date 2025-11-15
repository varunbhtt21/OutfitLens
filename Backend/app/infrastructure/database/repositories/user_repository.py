"""
User repository implementation.
Implements the UserRepository interface using SQLAlchemy.
"""

from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.domain.user.entities import User
from app.domain.user.value_objects import Email
from app.domain.user.repositories import UserRepository
from app.infrastructure.database.models import UserModel
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError, DatabaseError


class UserRepositoryImpl(UserRepository):
    """
    SQLAlchemy implementation of UserRepository.
    Handles conversion between domain entities and database models.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, user: User) -> User:
        """Create a new user in the database."""
        try:
            # Convert domain entity to database model
            user_model = self._to_model(user)

            self.db.add(user_model)
            self.db.commit()
            self.db.refresh(user_model)

            # Convert back to domain entity
            return self._to_entity(user_model)

        except IntegrityError as e:
            self.db.rollback()
            raise UserAlreadyExistsError(
                f"User with email {user.email.value} already exists"
            )
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create user: {str(e)}")

    def get_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        try:
            user_model = self.db.query(UserModel).filter(
                UserModel.id == user_id
            ).first()

            if not user_model:
                return None

            return self._to_entity(user_model)

        except Exception as e:
            raise DatabaseError(f"Failed to get user by ID: {str(e)}")

    def get_by_email(self, email: Email) -> Optional[User]:
        """Get user by email address."""
        try:
            user_model = self.db.query(UserModel).filter(
                UserModel.email == email.value
            ).first()

            if not user_model:
                return None

            return self._to_entity(user_model)

        except Exception as e:
            raise DatabaseError(f"Failed to get user by email: {str(e)}")

    def update(self, user: User) -> User:
        """Update an existing user."""
        try:
            user_model = self.db.query(UserModel).filter(
                UserModel.id == user.id
            ).first()

            if not user_model:
                raise UserNotFoundError(f"User with ID {user.id} not found")

            # Update model fields from entity
            user_model.email = user.email.value
            user_model.hashed_password = user.hashed_password
            user_model.full_name = user.full_name
            user_model.is_active = user.is_active
            user_model.is_verified = user.is_verified
            user_model.updated_at = user.updated_at

            self.db.commit()
            self.db.refresh(user_model)

            return self._to_entity(user_model)

        except UserNotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update user: {str(e)}")

    def delete(self, user_id: str) -> bool:
        """Delete a user by ID."""
        try:
            user_model = self.db.query(UserModel).filter(
                UserModel.id == user_id
            ).first()

            if not user_model:
                return False

            self.db.delete(user_model)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete user: {str(e)}")

    def exists_by_email(self, email: Email) -> bool:
        """Check if user with email exists."""
        try:
            count = self.db.query(UserModel).filter(
                UserModel.email == email.value
            ).count()

            return count > 0

        except Exception as e:
            raise DatabaseError(f"Failed to check user existence: {str(e)}")

    # Helper methods for conversion

    def _to_model(self, user: User) -> UserModel:
        """
        Convert domain entity to database model.

        Args:
            user: User domain entity

        Returns:
            UserModel database model
        """
        return UserModel(
            id=user.id,
            email=user.email.value,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    def _to_entity(self, model: UserModel) -> User:
        """
        Convert database model to domain entity.

        Args:
            model: UserModel database model

        Returns:
            User domain entity
        """
        return User(
            id=model.id,
            email=Email(model.email),
            hashed_password=model.hashed_password,
            full_name=model.full_name,
            is_active=model.is_active,
            is_verified=model.is_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
