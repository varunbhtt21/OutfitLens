"""
Image repository implementation.
Implements the ImageRepository interface using SQLAlchemy.
"""

from typing import Optional, List
from sqlalchemy.orm import Session

from app.domain.image.entities import Image, ImageMetadata
from app.domain.image.value_objects import (
    ImageFormat,
    ImageDimensions,
    ImageSize,
    ImageType,
)
from app.domain.image.repositories import ImageRepository
from app.infrastructure.database.models import ImageModel
from app.core.exceptions import ImageNotFoundError, DatabaseError


class ImageRepositoryImpl(ImageRepository):
    """
    SQLAlchemy implementation of ImageRepository.
    Handles conversion between domain entities and database models.
    """

    def __init__(self, db: Session):
        """
        Initialize repository with database session.

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def create(self, image: Image) -> Image:
        """Create a new image in the database."""
        try:
            # Convert domain entity to database model
            image_model = self._to_model(image)

            self.db.add(image_model)
            self.db.commit()
            self.db.refresh(image_model)

            # Convert back to domain entity
            return self._to_entity(image_model)

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to create image: {str(e)}")

    def get_by_id(self, image_id: str) -> Optional[Image]:
        """Get image by ID."""
        try:
            image_model = self.db.query(ImageModel).filter(
                ImageModel.id == image_id
            ).first()

            if not image_model:
                return None

            return self._to_entity(image_model)

        except Exception as e:
            raise DatabaseError(f"Failed to get image by ID: {str(e)}")

    def get_by_user(
        self, user_id: str, image_type: ImageType | None = None
    ) -> List[Image]:
        """Get all images for a user, optionally filtered by type."""
        try:
            query = self.db.query(ImageModel).filter(
                ImageModel.user_id == user_id
            )

            if image_type:
                query = query.filter(ImageModel.image_type == str(image_type))

            # Order by most recent first
            query = query.order_by(ImageModel.created_at.desc())

            image_models = query.all()

            return [self._to_entity(model) for model in image_models]

        except Exception as e:
            raise DatabaseError(f"Failed to get images by user: {str(e)}")

    def delete(self, image_id: str) -> bool:
        """Delete an image by ID."""
        try:
            image_model = self.db.query(ImageModel).filter(
                ImageModel.id == image_id
            ).first()

            if not image_model:
                return False

            self.db.delete(image_model)
            self.db.commit()

            return True

        except Exception as e:
            self.db.rollback()
            raise DatabaseError(f"Failed to delete image: {str(e)}")

    def exists(self, image_id: str) -> bool:
        """Check if image exists."""
        try:
            count = self.db.query(ImageModel).filter(
                ImageModel.id == image_id
            ).count()

            return count > 0

        except Exception as e:
            raise DatabaseError(f"Failed to check image existence: {str(e)}")

    # Helper methods for conversion

    def _to_model(self, image: Image) -> ImageModel:
        """
        Convert domain entity to database model.

        Args:
            image: Image domain entity

        Returns:
            ImageModel database model
        """
        return ImageModel(
            id=image.id,
            user_id=image.user_id,
            image_type=str(image.image_type),
            file_path=image.file_path,
            file_size=image.metadata.file_size.size_bytes,
            mime_type=image.metadata.mime_type,
            width=image.metadata.dimensions.width,
            height=image.metadata.dimensions.height,
            created_at=image.created_at,
        )

    def _to_entity(self, model: ImageModel) -> Image:
        """
        Convert database model to domain entity.

        Args:
            model: ImageModel database model

        Returns:
            Image domain entity
        """
        # Reconstruct metadata
        metadata = ImageMetadata(
            file_size=ImageSize(model.file_size or 0),
            dimensions=ImageDimensions(model.width or 0, model.height or 0),
            format=ImageFormat(model.file_path.split(".")[-1]),
            mime_type=model.mime_type or "application/octet-stream",
        )

        return Image(
            id=model.id,
            user_id=model.user_id,
            image_type=ImageType(model.image_type),
            file_path=model.file_path,
            metadata=metadata,
            created_at=model.created_at,
        )
