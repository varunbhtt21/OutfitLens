"""
Generation workflow application service.
Handles AI generation request creation, processing, and history use cases.
"""

import time
from typing import List
from pathlib import Path

from app.domain.generation.entities import Generation
from app.domain.generation.repositories import GenerationRepository
from app.domain.generation.services import GenerationDomainService
from app.domain.image.repositories import ImageRepository
from app.domain.image.value_objects import ImageType
from app.domain.image.entities import Image
from app.application.dtos.generation_dtos import (
    CreateGenerationDTO,
    GenerationDTO,
    GenerationStatusDTO,
    GenerationHistoryDTO,
)
from app.infrastructure.external.gemini_service import GeminiService
from app.infrastructure.storage.storage_interface import StorageInterface
from app.core.exceptions import (
    GenerationNotFoundError,
    AuthorizationError,
    ValidationError,
    GeminiAPIError,
)


class GenerationService:
    """
    Application service for generation workflow use cases.
    """

    def __init__(
        self,
        generation_repository: GenerationRepository,
        image_repository: ImageRepository,
        gemini_service: GeminiService,
        storage_service: StorageInterface,
        generation_domain_service: GenerationDomainService,
    ):
        """
        Initialize generation service.

        Args:
            generation_repository: Generation repository for data access
            image_repository: Image repository for data access
            gemini_service: Gemini AI service for image generation
            storage_service: Storage service for file operations
            generation_domain_service: Generation domain service for business logic
        """
        self.generation_repository = generation_repository
        self.image_repository = image_repository
        self.gemini_service = gemini_service
        self.storage_service = storage_service
        self.generation_domain_service = generation_domain_service

    def create_generation(self, dto: CreateGenerationDTO) -> GenerationDTO:
        """
        Create a new generation request.

        Args:
            dto: Generation creation data

        Returns:
            GenerationDTO with created generation information

        Raises:
            ValidationError: If request validation fails
        """
        # Validate generation request (domain service)
        try:
            self.generation_domain_service.validate_generation_request(
                dto.user_id, dto.user_photo_id, dto.clothing_photo_id
            )
        except ValueError as e:
            raise ValidationError(str(e))

        # Create generation entity (domain logic)
        generation = Generation.create(
            user_id=dto.user_id,
            user_photo_id=dto.user_photo_id,
            clothing_photo_id=dto.clothing_photo_id,
        )

        # Persist to database
        created_generation = self.generation_repository.create(generation)

        # Start processing asynchronously
        # Note: In production, this should use a background task queue (Celery, Redis Queue, etc.)
        # For now, we'll process synchronously
        try:
            self._process_generation(created_generation.id)
        except Exception as e:
            # If processing fails immediately, update generation status
            generation.fail(str(e))
            self.generation_repository.update(generation)

        # Fetch updated generation and return
        updated_generation = self.generation_repository.get_by_id(created_generation.id)
        return self._to_dto(updated_generation)

    def get_generation(
        self, generation_id: str, requesting_user_id: str
    ) -> GenerationDTO:
        """
        Get generation by ID.

        Args:
            generation_id: Generation's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            GenerationDTO with generation information

        Raises:
            GenerationNotFoundError: If generation doesn't exist
            AuthorizationError: If user doesn't own the generation
        """
        generation = self.generation_repository.get_by_id(generation_id)
        if not generation:
            raise GenerationNotFoundError(f"Generation not found: {generation_id}")

        # Verify user owns the generation
        if not generation.belongs_to_user(requesting_user_id):
            raise AuthorizationError("You don't have access to this generation")

        return self._to_dto(generation)

    def get_generation_status(
        self, generation_id: str, requesting_user_id: str
    ) -> GenerationStatusDTO:
        """
        Get generation status by ID.

        Args:
            generation_id: Generation's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            GenerationStatusDTO with status information

        Raises:
            GenerationNotFoundError: If generation doesn't exist
            AuthorizationError: If user doesn't own the generation
        """
        generation = self.generation_repository.get_by_id(generation_id)
        if not generation:
            raise GenerationNotFoundError(f"Generation not found: {generation_id}")

        # Verify user owns the generation
        if not generation.belongs_to_user(requesting_user_id):
            raise AuthorizationError("You don't have access to this generation")

        return GenerationStatusDTO(
            id=generation.id,
            status=str(generation.status),
            error_message=generation.error_message,
        )

    def get_generation_history(
        self, user_id: str, page: int = 1, page_size: int = 20
    ) -> GenerationHistoryDTO:
        """
        Get generation history for a user with pagination.

        Args:
            user_id: User's unique identifier
            page: Page number (1-indexed)
            page_size: Number of items per page

        Returns:
            GenerationHistoryDTO with paginated history
        """
        # Calculate offset
        offset = (page - 1) * page_size

        # Get generations with pagination
        generations = self.generation_repository.get_by_user(
            user_id, limit=page_size, offset=offset
        )

        # Get total count
        total = self.generation_repository.count_by_user(user_id)

        # Calculate if there are more pages
        has_more = (offset + len(generations)) < total

        # Convert to DTOs
        generation_dtos = [self._to_dto(gen) for gen in generations]

        return GenerationHistoryDTO(
            items=generation_dtos,
            total=total,
            page=page,
            page_size=page_size,
            has_more=has_more,
        )

    def delete_generation(
        self, generation_id: str, requesting_user_id: str
    ) -> bool:
        """
        Delete a generation.

        Args:
            generation_id: Generation's unique identifier
            requesting_user_id: ID of user making the request

        Returns:
            True if generation was deleted

        Raises:
            GenerationNotFoundError: If generation doesn't exist
            AuthorizationError: If user doesn't own the generation
        """
        generation = self.generation_repository.get_by_id(generation_id)
        if not generation:
            raise GenerationNotFoundError(f"Generation not found: {generation_id}")

        # Verify user owns the generation
        if not generation.belongs_to_user(requesting_user_id):
            raise AuthorizationError("You don't have access to this generation")

        # Delete result image if exists
        if generation.result_image_id:
            result_image = self.image_repository.get_by_id(generation.result_image_id)
            if result_image:
                self.storage_service.delete(result_image.file_path)
                self.image_repository.delete(result_image.id)

        # Delete generation from database
        deleted = self.generation_repository.delete(generation_id)

        return deleted

    # Private helper methods

    def _process_generation(self, generation_id: str) -> None:
        """
        Process a generation request (internal method).
        This should be moved to a background task in production.

        Args:
            generation_id: Generation's unique identifier
        """
        # Get generation
        generation = self.generation_repository.get_by_id(generation_id)
        if not generation:
            return

        try:
            # Mark as processing
            generation.start_processing()
            self.generation_repository.update(generation)

            # Get image paths
            user_photo = self.image_repository.get_by_id(generation.user_photo_id)
            clothing_photo = self.image_repository.get_by_id(
                generation.clothing_photo_id
            )

            if not user_photo or not clothing_photo:
                raise ValueError("Required images not found")

            # Get full paths from storage
            from app.infrastructure.storage.local_storage import LocalStorageService
            if isinstance(self.storage_service, LocalStorageService):
                user_photo_path = self.storage_service.get_full_path(
                    user_photo.file_path
                )
                clothing_photo_path = self.storage_service.get_full_path(
                    clothing_photo.file_path
                )
            else:
                user_photo_path = Path(user_photo.file_path)
                clothing_photo_path = Path(clothing_photo.file_path)

            # Call Gemini AI service
            start_time = time.time()

            result_image_bytes = self.gemini_service.generate_virtual_tryon(
                user_photo_path, clothing_photo_path
            )

            processing_time_ms = int((time.time() - start_time) * 1000)

            # Save result image
            result_file_path = self.storage_service.generate_unique_path(
                generation.user_id, "generated_result", "result.png"
            )

            import io
            result_file = io.BytesIO(result_image_bytes)
            self.storage_service.save(result_file, result_file_path)

            # Create result image entity
            from app.domain.image.entities import ImageMetadata
            from app.domain.image.value_objects import (
                ImageFormat,
                ImageDimensions,
                ImageSize,
            )

            # Extract metadata from result
            result_file.seek(0)
            from PIL import Image as PILImage
            with PILImage.open(result_file) as img:
                width, height = img.size

            result_metadata = ImageMetadata(
                file_size=ImageSize(len(result_image_bytes)),
                dimensions=ImageDimensions(width, height),
                format=ImageFormat("png"),
                mime_type="image/png",
            )

            result_image = Image.create(
                user_id=generation.user_id,
                image_type=ImageType("generated_result"),
                file_path=result_file_path,
                metadata=result_metadata,
            )

            created_result_image = self.image_repository.create(result_image)

            # Mark generation as completed
            generation.complete(created_result_image.id, processing_time_ms)
            self.generation_repository.update(generation)

        except GeminiAPIError as e:
            # AI service error
            generation.fail(f"AI generation failed: {str(e)}")
            self.generation_repository.update(generation)

        except Exception as e:
            # Other error
            generation.fail(f"Generation failed: {str(e)}")
            self.generation_repository.update(generation)

    def _to_dto(self, generation: Generation) -> GenerationDTO:
        """Convert Generation entity to GenerationDTO."""
        # Get images
        user_photo = self.image_repository.get_by_id(generation.user_photo_id)
        clothing_photo = self.image_repository.get_by_id(
            generation.clothing_photo_id
        )
        result_image = (
            self.image_repository.get_by_id(generation.result_image_id)
            if generation.result_image_id
            else None
        )

        # Convert images to DTOs
        from app.application.dtos.image_dtos import ImageDTO

        user_photo_dto = self._image_to_dto(user_photo) if user_photo else None
        clothing_photo_dto = (
            self._image_to_dto(clothing_photo) if clothing_photo else None
        )
        result_image_dto = self._image_to_dto(result_image) if result_image else None

        return GenerationDTO(
            id=generation.id,
            user_id=generation.user_id,
            status=str(generation.status),
            user_photo=user_photo_dto,
            clothing_photo=clothing_photo_dto,
            result_image=result_image_dto,
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

    def _image_to_dto(self, image: Image) -> "ImageDTO":
        """Convert Image entity to ImageDTO."""
        from app.application.dtos.image_dtos import ImageDTO

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
