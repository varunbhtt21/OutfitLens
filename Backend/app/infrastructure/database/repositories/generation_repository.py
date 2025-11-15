"""
Generation repository implementation.
Implements the GenerationRepository interface using SQLAlchemy.
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.generation.entities import Generation
from app.domain.generation.value_objects import GenerationStatus, ProcessingTime
from app.domain.generation.repositories import GenerationRepository
from app.infrastructure.database.models import GenerationModel
from app.core.exceptions import GenerationNotFoundError, DatabaseError


class GenerationRepositoryImpl(GenerationRepository):
    """
    SQLAlchemy implementation of GenerationRepository.
    Handles conversion between domain entities and database models.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, generation: Generation) -> Generation:
        """Create a new generation in the database."""
        try:
            # Convert domain entity to database model
            generation_model = self._to_model(generation)

            self.db.add(generation_model)
            self.db.commit()
            self.db.refresh(generation_model)

            # Convert back to domain entity
            return self._to_entity(generation_model)

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create generation: {str(e)}")

    def get_by_id(self, generation_id: str) -> Optional[Generation]:
        """Get generation by ID."""
        try:
            generation_model = self.db.query(GenerationModel).filter(
                GenerationModel.id == generation_id
            ).first()

            if not generation_model:
                return None

            return self._to_entity(generation_model)

        except Exception as e:
            raise DatabaseError(f"Failed to get generation by ID: {str(e)}")

    def get_by_user(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> List[Generation]:
        """Get all generations for a user with pagination."""
        try:
            query = self.db.query(GenerationModel).filter(
                GenerationModel.user_id == user_id
            )

            # Order by most recent first
            query = query.order_by(GenerationModel.created_at.desc())

            # Apply pagination
            query = query.limit(limit).offset(offset)

            generation_models = query.all()

            return [self._to_entity(model) for model in generation_models]

        except Exception as e:
            raise DatabaseError(f"Failed to get generations by user: {str(e)}")

    def update(self, generation: Generation) -> Generation:
        """Update an existing generation."""
        try:
            generation_model = self.db.query(GenerationModel).filter(
                GenerationModel.id == generation.id
            ).first()

            if not generation_model:
                raise GenerationNotFoundError(
                    f"Generation with ID {generation.id} not found"
                )

            # Update model fields from entity
            generation_model.status = str(generation.status)
            generation_model.result_image_id = generation.result_image_id
            generation_model.error_message = generation.error_message
            generation_model.processing_time_ms = (
                generation.processing_time.milliseconds
                if generation.processing_time
                else None
            )
            generation_model.updated_at = generation.updated_at
            generation_model.completed_at = generation.completed_at

            self.db.commit()
            self.db.refresh(generation_model)

            return self._to_entity(generation_model)

        except GenerationNotFoundError:
            raise
        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to update generation: {str(e)}")

    def delete(self, generation_id: str) -> bool:
        """Delete a generation by ID."""
        try:
            generation_model = self.db.query(GenerationModel).filter(
                GenerationModel.id == generation_id
            ).first()

            if not generation_model:
                return False

            self.db.delete(generation_model)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete generation: {str(e)}")

    def count_by_user(self, user_id: str) -> int:
        """Count total generations for a user."""
        try:
            count = self.db.query(GenerationModel).filter(
                GenerationModel.user_id == user_id
            ).count()

            return count

        except Exception as e:
            raise DatabaseError(f"Failed to count generations: {str(e)}")

    # Helper methods for conversion

    def _to_model(self, generation: Generation) -> GenerationModel:
        """
        Convert domain entity to database model.

        Args:
            generation: Generation domain entity

        Returns:
            GenerationModel database model
        """
        return GenerationModel(
            id=generation.id,
            user_id=generation.user_id,
            user_photo_id=generation.user_photo_id,
            clothing_photo_id=generation.clothing_photo_id,
            result_image_id=generation.result_image_id,
            status=str(generation.status),
            error_message=generation.error_message,
            processing_time_ms=(
                generation.processing_time.milliseconds
                if generation.processing_time
                else None
            ),
            created_at=generation.created_at,
            updated_at=generation.updated_at,
            completed_at=generation.completed_at,
        )

    def _to_entity(self, model: GenerationModel) -> Generation:
        """
        Convert database model to domain entity.

        Args:
            model: GenerationModel database model

        Returns:
            Generation domain entity
        """
        return Generation(
            id=model.id,
            user_id=model.user_id,
            user_photo_id=model.user_photo_id,
            clothing_photo_id=model.clothing_photo_id,
            status=GenerationStatus(model.status),
            result_image_id=model.result_image_id,
            error_message=model.error_message,
            processing_time=(
                ProcessingTime(model.processing_time_ms)
                if model.processing_time_ms is not None
                else None
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
            completed_at=model.completed_at,
        )
