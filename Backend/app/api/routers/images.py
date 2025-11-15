"""
Image API routes.
Handles image upload, retrieval, and management.
"""

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import FileResponse

from app.api.schemas.image_schemas import (
    ImageResponse,
    UploadImageResponse,
    ImageListResponse,
)
from app.api.schemas.user_schemas import MessageResponse
from app.api.dependencies import get_image_service, get_storage_service, CurrentUser
from app.application.services.image_service import ImageService
from app.infrastructure.storage.local_storage import LocalStorageService
from app.core.exceptions import (
    ImageNotFoundError,
    InvalidImageFormatError,
    InvalidImageSizeError,
    AuthorizationError,
)

router = APIRouter(prefix="/images", tags=["Images"])


@router.post(
    "/upload/user-photo",
    response_model=UploadImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload user photo",
    description="Upload a photo of the user for virtual try-on",
)
async def upload_user_photo(
    current_user_id: CurrentUser,
    image_service: ImageService = Depends(get_image_service),
    file: UploadFile = File(..., description="Image file (JPG, PNG, WEBP, max 10MB)"),
) -> UploadImageResponse:
    """Upload a user photo."""
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)

        # Create file-like object
        import io
        file_obj = io.BytesIO(content)

        # Upload image
        image_dto = image_service.upload_user_photo(
            user_id=current_user_id,
            file=file_obj,
            filename=file.filename or "image.jpg",
            file_size=file_size,
        )

        return UploadImageResponse(
            id=image_dto.id,
            image_type=image_dto.image_type,
            file_size=image_dto.file_size,
            width=image_dto.width,
            height=image_dto.height,
            url=image_dto.url,
        )

    except InvalidImageFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except InvalidImageSizeError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )


@router.post(
    "/upload/clothing-photo",
    response_model=UploadImageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload clothing photo",
    description="Upload a photo of a clothing item for virtual try-on",
)
async def upload_clothing_photo(
    current_user_id: CurrentUser,
    image_service: ImageService = Depends(get_image_service),
    file: UploadFile = File(..., description="Image file (JPG, PNG, WEBP, max 10MB)"),
) -> UploadImageResponse:
    """Upload a clothing photo."""
    try:
        # Read file content
        content = await file.read()
        file_size = len(content)

        # Create file-like object
        import io
        file_obj = io.BytesIO(content)

        # Upload image
        image_dto = image_service.upload_clothing_photo(
            user_id=current_user_id,
            file=file_obj,
            filename=file.filename or "image.jpg",
            file_size=file_size,
        )

        return UploadImageResponse(
            id=image_dto.id,
            image_type=image_dto.image_type,
            file_size=image_dto.file_size,
            width=image_dto.width,
            height=image_dto.height,
            url=image_dto.url,
        )

    except InvalidImageFormatError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except InvalidImageSizeError as e:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=str(e),
        )


@router.get(
    "/{image_id}",
    response_class=FileResponse,
    summary="Get image file",
    description="Download an image file by ID",
)
async def get_image_file(
    image_id: str,
    current_user_id: CurrentUser,
    image_service: ImageService = Depends(get_image_service),
    storage_service: LocalStorageService = Depends(get_storage_service),
) -> FileResponse:
    """Get image file."""
    try:
        # Get image metadata
        image_dto = image_service.get_image(image_id, current_user_id)

        # Get full file path
        full_path = storage_service.get_full_path(image_dto.file_path)

        return FileResponse(
            path=str(full_path),
            media_type=image_dto.mime_type,
            filename=f"{image_id}.{image_dto.file_path.split('.')[-1]}",
        )

    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.get(
    "",
    response_model=ImageListResponse,
    summary="Get user images",
    description="Get all images for the authenticated user",
)
async def get_user_images(
    current_user_id: CurrentUser,
    image_service: ImageService = Depends(get_image_service),
    image_type: str | None = Query(
        None, description="Filter by image type (user_photo, clothing_photo)"
    ),
) -> ImageListResponse:
    """Get all images for current user."""
    try:
        image_dtos = image_service.get_user_images(current_user_id, image_type)

        images = [
            ImageResponse(
                id=img.id,
                user_id=img.user_id,
                image_type=img.image_type,
                file_path=img.file_path,
                file_size=img.file_size,
                mime_type=img.mime_type,
                width=img.width,
                height=img.height,
                created_at=img.created_at,
                url=img.url,
            )
            for img in image_dtos
        ]

        return ImageListResponse(images=images, total=len(images))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve images: {str(e)}",
        )


@router.delete(
    "/{image_id}",
    response_model=MessageResponse,
    summary="Delete image",
    description="Delete an image by ID",
)
async def delete_image(
    image_id: str,
    current_user_id: CurrentUser,
    image_service: ImageService = Depends(get_image_service),
) -> MessageResponse:
    """Delete an image."""
    try:
        image_service.delete_image(image_id, current_user_id)

        return MessageResponse(message="Image deleted successfully")

    except ImageNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
