"""
Generation domain services.
"""

from app.domain.generation.repositories import GenerationRepository
from app.domain.image.repositories import ImageRepository
from app.domain.shared.enums import ImageTypeEnum


class GenerationDomainService:
    """
    Domain service for Generation-related business logic.
    """

    def __init__(
        self,
        generation_repository: GenerationRepository,
        image_repository: ImageRepository,
    ):
        """
        Initialize domain service.

        Args:
            generation_repository: Generation repository for data access
            image_repository: Image repository for validating images
        """
        self.generation_repository = generation_repository
        self.image_repository = image_repository

    def can_create_generation(self, user_id: str) -> bool:
        """
        Check if a user can create a new generation.
        Business rules for rate limiting or quotas can be added here.

        Args:
            user_id: User's unique identifier

        Returns:
            True if user can create generation, False otherwise
        """
        # For now, any user can create a generation
        # In the future, might add rate limiting, quotas, etc.
        return True

    def validate_generation_request(
        self, user_id: str, user_photo_id: str, clothing_photo_id: str
    ) -> bool:
        """
        Validate that a generation request is valid.

        Args:
            user_id: User's unique identifier
            user_photo_id: ID of user's photo
            clothing_photo_id: ID of clothing photo

        Returns:
            True if request is valid

        Raises:
            ValueError: If validation fails
        """
        # Check that both images exist
        user_photo = self.image_repository.get_by_id(user_photo_id)
        if not user_photo:
            raise ValueError(f"User photo not found: {user_photo_id}")

        clothing_photo = self.image_repository.get_by_id(clothing_photo_id)
        if not clothing_photo:
            raise ValueError(f"Clothing photo not found: {clothing_photo_id}")

        # Check that user owns both images
        if not user_photo.belongs_to_user(user_id):
            raise ValueError("User does not own the user photo")

        if not clothing_photo.belongs_to_user(user_id):
            raise ValueError("User does not own the clothing photo")

        # Check that image types are correct
        if not user_photo.image_type.is_user_photo():
            raise ValueError(
                f"Image {user_photo_id} is not a user photo (type: {user_photo.image_type})"
            )

        if not clothing_photo.image_type.is_clothing_photo():
            raise ValueError(
                f"Image {clothing_photo_id} is not a clothing photo (type: {clothing_photo.image_type})"
            )

        return True
