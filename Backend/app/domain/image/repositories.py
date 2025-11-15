"""
Image repository interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.image.entities import Image
from app.domain.image.value_objects import ImageType


class ImageRepository(ABC):
    """
    Repository interface for Image aggregate.
    Infrastructure layer will implement this interface.
    """

    @abstractmethod
    def create(self, image: Image) -> Image:
        """
        Create a new image.

        Args:
            image: Image entity to persist

        Returns:
            Created image entity

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, image_id: str) -> Optional[Image]:
        """
        Get image by ID.

        Args:
            image_id: Image's unique identifier

        Returns:
            Image entity if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_user(
        self, user_id: str, image_type: ImageType | None = None
    ) -> List[Image]:
        """
        Get all images for a user, optionally filtered by type.

        Args:
            user_id: User's unique identifier
            image_type: Optional image type to filter by

        Returns:
            List of Image entities
        """
        pass

    @abstractmethod
    def delete(self, image_id: str) -> bool:
        """
        Delete an image by ID.

        Args:
            image_id: Image's unique identifier

        Returns:
            True if deleted, False if image not found
        """
        pass

    @abstractmethod
    def exists(self, image_id: str) -> bool:
        """
        Check if image exists.

        Args:
            image_id: Image's unique identifier

        Returns:
            True if image exists, False otherwise
        """
        pass
