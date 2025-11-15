"""
User API routes.
Handles user profile and account management.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.user_schemas import (
    UserResponse,
    UpdateUserRequest,
    ChangePasswordRequest,
    MessageResponse,
)
from app.api.dependencies import get_user_service, CurrentUser
from app.application.services.user_service import UserService
from app.application.dtos.user_dtos import UpdateUserDTO, ChangePasswordDTO
from app.core.exceptions import (
    UserNotFoundError,
    InvalidCredentialsError,
    InvalidPasswordError,
    AuthorizationError,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user profile",
    description="Get the authenticated user's profile information",
)
async def get_current_user_profile(
    current_user_id: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Get current user's profile."""
    try:
        user_dto = user_service.get_user_profile(current_user_id)

        return UserResponse(
            id=user_dto.id,
            email=user_dto.email,
            full_name=user_dto.full_name,
            is_active=user_dto.is_active,
            is_verified=user_dto.is_verified,
            created_at=user_dto.created_at,
            updated_at=user_dto.updated_at,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Update user profile",
    description="Update the authenticated user's profile information",
)
async def update_user_profile(
    request: UpdateUserRequest,
    current_user_id: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update current user's profile."""
    try:
        dto = UpdateUserDTO(full_name=request.full_name)
        user_dto = user_service.update_user_profile(current_user_id, dto)

        return UserResponse(
            id=user_dto.id,
            email=user_dto.email,
            full_name=user_dto.full_name,
            is_active=user_dto.is_active,
            is_verified=user_dto.is_verified,
            created_at=user_dto.created_at,
            updated_at=user_dto.updated_at,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.patch(
    "/me/password",
    response_model=MessageResponse,
    summary="Change password",
    description="Change the authenticated user's password",
)
async def change_password(
    request: ChangePasswordRequest,
    current_user_id: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> MessageResponse:
    """Change current user's password."""
    try:
        dto = ChangePasswordDTO(
            old_password=request.old_password,
            new_password=request.new_password,
        )
        user_service.change_password(current_user_id, dto)

        return MessageResponse(message="Password changed successfully")

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except InvalidPasswordError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.delete(
    "/me",
    response_model=MessageResponse,
    summary="Delete user account",
    description="Delete the authenticated user's account",
)
async def delete_user_account(
    current_user_id: CurrentUser,
    user_service: UserService = Depends(get_user_service),
) -> MessageResponse:
    """Delete current user's account."""
    try:
        user_service.delete_user_account(current_user_id, current_user_id)

        return MessageResponse(message="Account deleted successfully")

    except AuthorizationError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
