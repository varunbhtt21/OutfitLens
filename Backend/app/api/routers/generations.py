"""
Generation API routes.
Handles AI generation creation, status, and history.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.api.schemas.generation_schemas import (
    CreateGenerationRequest,
    GenerationResponse,
    GenerationStatusResponse,
    GenerationHistoryResponse,
)
from app.api.schemas.user_schemas import MessageResponse
from app.api.schemas.image_schemas import ImageResponse
from app.api.dependencies import get_generation_service, CurrentUser
from app.application.services.generation_service import GenerationService
from app.application.dtos.generation_dtos import CreateGenerationDTO
from app.core.exceptions import (
    GenerationNotFoundError,
    AuthorizationError,
    ValidationError,
)

router = APIRouter(prefix="/generations", tags=["Generations"])


@router.post(
    "",
    response_model=GenerationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create generation",
    description="Create a new AI virtual try-on generation request",
)
async def create_generation(
    request: CreateGenerationRequest,
    current_user_id: CurrentUser,
    generation_service: GenerationService = Depends(get_generation_service),
) -> GenerationResponse:
    """Create a new generation request."""
    try:
        dto = CreateGenerationDTO(
            user_id=current_user_id,
            user_photo_id=request.user_photo_id,
            clothing_photo_id=request.clothing_photo_id,
        )

        generation_dto = generation_service.create_generation(dto)

        return _map_to_response(generation_dto)

    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.get(
    "/{generation_id}",
    response_model=GenerationResponse,
    summary="Get generation",
    description="Get generation details by ID",
)
async def get_generation(
    generation_id: str,
    current_user_id: CurrentUser,
    generation_service: GenerationService = Depends(get_generation_service),
) -> GenerationResponse:
    """Get generation by ID."""
    try:
        generation_dto = generation_service.get_generation(
            generation_id, current_user_id
        )

        return _map_to_response(generation_dto)

    except GenerationNotFoundError as e:
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
    "/{generation_id}/status",
    response_model=GenerationStatusResponse,
    summary="Get generation status",
    description="Get the current status of a generation",
)
async def get_generation_status(
    generation_id: str,
    current_user_id: CurrentUser,
    generation_service: GenerationService = Depends(get_generation_service),
) -> GenerationStatusResponse:
    """Get generation status."""
    try:
        status_dto = generation_service.get_generation_status(
            generation_id, current_user_id
        )

        return GenerationStatusResponse(
            id=status_dto.id,
            status=status_dto.status,
            error_message=status_dto.error_message,
        )

    except GenerationNotFoundError as e:
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
    response_model=GenerationHistoryResponse,
    summary="Get generation history",
    description="Get paginated generation history for the authenticated user",
)
async def get_generation_history(
    current_user_id: CurrentUser,
    generation_service: GenerationService = Depends(get_generation_service),
    page: int = Query(1, ge=1, description="Page number (1-indexed)"),
    page_size: int = Query(20, ge=1, le=100, description="Items per page"),
) -> GenerationHistoryResponse:
    """Get generation history."""
    try:
        history_dto = generation_service.get_generation_history(
            current_user_id, page, page_size
        )

        items = [_map_to_response(gen) for gen in history_dto.items]

        return GenerationHistoryResponse(
            items=items,
            total=history_dto.total,
            page=history_dto.page,
            page_size=history_dto.page_size,
            has_more=history_dto.has_more,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve generation history: {str(e)}",
        )


@router.delete(
    "/{generation_id}",
    response_model=MessageResponse,
    summary="Delete generation",
    description="Delete a generation by ID",
)
async def delete_generation(
    generation_id: str,
    current_user_id: CurrentUser,
    generation_service: GenerationService = Depends(get_generation_service),
) -> MessageResponse:
    """Delete a generation."""
    try:
        generation_service.delete_generation(generation_id, current_user_id)

        return MessageResponse(message="Generation deleted successfully")

    except GenerationNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


# Helper function to map DTO to response
def _map_to_response(generation_dto) -> GenerationResponse:
    """Map GenerationDTO to GenerationResponse."""
    return GenerationResponse(
        id=generation_dto.id,
        user_id=generation_dto.user_id,
        status=generation_dto.status,
        user_photo=ImageResponse(
            id=generation_dto.user_photo.id,
            user_id=generation_dto.user_photo.user_id,
            image_type=generation_dto.user_photo.image_type,
            file_path=generation_dto.user_photo.file_path,
            file_size=generation_dto.user_photo.file_size,
            mime_type=generation_dto.user_photo.mime_type,
            width=generation_dto.user_photo.width,
            height=generation_dto.user_photo.height,
            created_at=generation_dto.user_photo.created_at,
            url=generation_dto.user_photo.url,
        ),
        clothing_photo=ImageResponse(
            id=generation_dto.clothing_photo.id,
            user_id=generation_dto.clothing_photo.user_id,
            image_type=generation_dto.clothing_photo.image_type,
            file_path=generation_dto.clothing_photo.file_path,
            file_size=generation_dto.clothing_photo.file_size,
            mime_type=generation_dto.clothing_photo.mime_type,
            width=generation_dto.clothing_photo.width,
            height=generation_dto.clothing_photo.height,
            created_at=generation_dto.clothing_photo.created_at,
            url=generation_dto.clothing_photo.url,
        ),
        result_image=(
            ImageResponse(
                id=generation_dto.result_image.id,
                user_id=generation_dto.result_image.user_id,
                image_type=generation_dto.result_image.image_type,
                file_path=generation_dto.result_image.file_path,
                file_size=generation_dto.result_image.file_size,
                mime_type=generation_dto.result_image.mime_type,
                width=generation_dto.result_image.width,
                height=generation_dto.result_image.height,
                created_at=generation_dto.result_image.created_at,
                url=generation_dto.result_image.url,
            )
            if generation_dto.result_image
            else None
        ),
        error_message=generation_dto.error_message,
        processing_time_ms=generation_dto.processing_time_ms,
        created_at=generation_dto.created_at,
        updated_at=generation_dto.updated_at,
        completed_at=generation_dto.completed_at,
    )
