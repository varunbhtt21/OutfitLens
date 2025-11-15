"""
Image domain entities.
"""

from datetime import datetime
from app.domain.shared.base import AggregateRoot
from app.domain.image.value_objects import (
    ImageFormat,
    ImageDimensions,
    ImageSize,
    ImageType,
)
from app.domain.shared.events import ImageUploadedEvent


class ImageMetadata:
    """
    Image metadata entity.
    Contains technical details about the image.
    """

    def __init__(
        self,
        file_size: ImageSize,
        dimensions: ImageDimensions,
        format: ImageFormat,
        mime_type: str,
    ):
        """
        Create ImageMetadata.

        Args:
            file_size: Size of the image file
            dimensions: Width and height of the image
            format: Image format
            mime_type: MIME type of the image
        """
        self.file_size = file_size
        self.dimensions = dimensions
        self.format = format
        self.mime_type = mime_type

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"ImageMetadata(size={self.file_size}, dimensions={self.dimensions}, "
            f"format={self.format})"
        )


class Image(AggregateRoot):
    """
    Image aggregate root.
    Represents an uploaded image (user photo, clothing photo, or generated result).
    """

    def __init__(
        self,
        user_id: str,
        image_type: ImageType,
        file_path: str,
        metadata: ImageMetadata,
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        """
        Create an Image entity.

        Args:
            user_id: ID of the user who owns this image
            image_type: Type of image
            file_path: Path where image is stored
            metadata: Image metadata
            id: Unique identifier (generates if not provided)
            created_at: Creation timestamp (sets to now if not provided)
        """
        super().__init__(id)

        self.user_id = user_id
        self.image_type = image_type
        self.file_path = file_path
        self.metadata = metadata

        if created_at:
            self.created_at = created_at

    @staticmethod
    def create(
        user_id: str,
        image_type: ImageType,
        file_path: str,
        metadata: ImageMetadata,
    ) -> "Image":
        """
        Factory method to create a new image.

        Args:
            user_id: ID of the user who owns this image
            image_type: Type of image
            file_path: Path where image is stored
            metadata: Image metadata

        Returns:
            New Image instance with ImageUploadedEvent added
        """
        image = Image(
            user_id=user_id,
            image_type=image_type,
            file_path=file_path,
            metadata=metadata,
        )

        # Add domain event
        image.add_domain_event(
            ImageUploadedEvent.create(image.id, user_id, str(image_type))
        )

        return image

    def belongs_to_user(self, user_id: str) -> bool:
        """
        Check if image belongs to a specific user.

        Args:
            user_id: User ID to check

        Returns:
            True if image belongs to user, False otherwise
        """
        return self.user_id == user_id

    def get_url(self, base_url: str = "") -> str:
        """
        Get the URL for this image.

        Args:
            base_url: Base URL for image serving

        Returns:
            Full URL to the image
        """
        return f"{base_url}/{self.file_path}"

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Image(id={self.id!r}, type={self.image_type}, "
            f"user_id={self.user_id!r})"
        )
