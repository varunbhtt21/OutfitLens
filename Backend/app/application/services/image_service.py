"""
Image management application service.
Handles image upload, retrieval, and management use cases.
"""

from typing import BinaryIO, List

from app.domain.image.entities import Image
from app.domain.image.value_objects import ImageType
from app.domain.image.repositories import ImageRepository
from app.domain.image.services import ImageDomainService
from app.application.dtos.image_dtos import ImageDTO
from app.infrastructure.storage.storage_interface import StorageInterface
from app.core.exceptions import (
    ImageNotFoundError,
    AuthorizationError,
    InvalidImageFormatError,
)


class ImageService:
    """
    Application service for image management use cases.
    """

    def __init__(
        self,
        image_repository: ImageRepository,
        storage_service: StorageInterface,
        image_domain_service: ImageDomainService,
    ):
        """
        Initialize image service.

        Args:
            image_repository: Image repository for data access
            storage_service: Storage service for file operations
            image_domain_service: Image domain service for business logic
        """
        self.image_repository = image_repository
        self.storage_service = storage_service
        self.image_domain_service = image_domain_service

    def upload_user_photo(
        self, user_id: str, file: BinaryIO, filename: str, file_size: int
    ) -> ImageDTO:
        """
        Upload a user photo.

        Args:
            user_id: User's unique identifier
            file: File-like object containing image data
            filename: Original filename
            file_size: Size of file in bytes

        Returns:
            ImageDTO with uploaded image information

        Raises:
            InvalidImageFormatError: If image format is not supported
            InvalidImageSizeError: If image size exceeds maximum
        """
        return self._upload_image(
            user_id=user_id,
            file=file,
            filename=filename,
            file_size=file_size,
            image_type="user_photo",
        )

    def upload_clothing_photo(
        self, user_id: str, file: BinaryIO, filename: str, file_size: int
    ) -> ImageDTO:
        """
        Upload a clothing photo.

        Args:
            user_id: User's unique identifier
            file: File-like object containing image data
            filename: Original filename
            file_size: Size of file in bytes

        Returns:
            ImageDTO with uploaded image information

        Raises:
            InvalidImageFormatError: If image format is not supported
            InvalidImageSizeError: If image size exceeds maximum
        """
        return self._upload_image(
            user_id=user_id,
            file=file,
            filename=filename,
            file_size=file_size,
            image_type="clothing_photo",
        )

    def get_image(self, image_id: str, requesting_user_id: str) -> ImageDTO:
        """
        Get image by ID.

        Args:
            image_id: Image's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            ImageDTO with image information

        Raises:
            ImageNotFoundError: If image doesn't exist
            AuthorizationError: If user doesn't own the image
        """
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise ImageNotFoundError(f"Image not found: {image_id}")

        # Verify user owns the image
        if not image.belongs_to_user(requesting_user_id):
            raise AuthorizationError("You don't have access to this image")

        return self._to_dto(image)

    def get_user_images(
        self, user_id: str, image_type: str | None = None
    ) -> List[ImageDTO]:
        """
        Get all images for a user, optionally filtered by type.

        Args:
            user_id: User's unique identifier
            image_type: Optional image type to filter by

        Returns:
            List of ImageDTOs
        """
        image_type_vo = ImageType(image_type) if image_type else None
        images = self.image_repository.get_by_user(user_id, image_type_vo)

        return [self._to_dto(image) for image in images]

    def delete_image(self, image_id: str, requesting_user_id: str) -> bool:
        """
        Delete an image.

        Args:
            image_id: Image's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            True if image was deleted

        Raises:
            ImageNotFoundError: If image doesn't exist
            AuthorizationError: If user doesn't own the image
        """
        image = self.image_repository.get_by_id(image_id)
        if not image:
            raise ImageNotFoundError(f"Image not found: {image_id}")

        # Verify user owns the image
        if not image.belongs_to_user(requesting_user_id):
            raise AuthorizationError("You don't have access to this image")

        # Delete file from storage
        self.storage_service.delete(image.file_path)

        # Delete from database
        deleted = self.image_repository.delete(image_id)

        return deleted

    # Private helper methods

    def _upload_image(
        self,
        user_id: str,
        file: BinaryIO,
        filename: str,
        file_size: int,
        image_type: str,
    ) -> ImageDTO:
        """
        Internal method to handle image upload.

        Args:
            user_id: User's unique identifier
            file: File-like object containing image data
            filename: Original filename
            file_size: Size of file in bytes
            image_type: Type of image (user_photo, clothing_photo)

        Returns:
            ImageDTO with uploaded image information
        """
        # Extract and validate metadata (domain service)
        metadata = self.image_domain_service.extract_metadata(
            file, filename, file_size
        )

        # Generate unique file path
        from app.infrastructure.storage.local_storage import LocalStorageService
        if isinstance(self.storage_service, LocalStorageService):
            file_path = self.storage_service.generate_unique_path(
                user_id, image_type, filename
            )
        else:
            # For other storage services, use a simple path
            import uuid
            extension = filename.rsplit(".", 1)[-1] if "." in filename else "jpg"
            file_path = f"{image_type}/{user_id}/{uuid.uuid4()}.{extension}"

        # Reset file pointer to beginning
        file.seek(0)

        # Save file to storage
        self.storage_service.save(file, file_path)

        # Create image entity (domain logic)
        image = Image.create(
            user_id=user_id,
            image_type=ImageType(image_type),
            file_path=file_path,
            metadata=metadata,
        )

        # Persist to database
        created_image = self.image_repository.create(image)

        return self._to_dto(created_image)

    def _to_dto(self, image: Image) -> ImageDTO:
        """Convert Image entity to ImageDTO."""
        return ImageDTO(
            id=image.id,
            user_id=image.user_id,
            image_type=str(image.image_type),
            file_path=image.file_path,
            file_size=image.metadata.file_size.size_bytes,
            mime_type=image.metadata.mime_type,
            width=image.metadata.dimensions.width,
            height=image.metadata.dimensions.height,
            created_at=image.created_at,
            url=self.storage_service.get_url(image.file_path),
        )
