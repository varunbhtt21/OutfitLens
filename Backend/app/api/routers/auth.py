"""
Authentication API routes.
Handles user registration, login, and token management.
"""

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.schemas.auth_schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
    RefreshTokenRequest,
    AccessTokenResponse,
)
from app.api.schemas.user_schemas import UserResponse
from app.api.dependencies import get_auth_service
from app.application.services.auth_service import AuthService
from app.application.dtos.user_dtos import CreateUserDTO
from app.core.exceptions import (
    UserAlreadyExistsError,
    InvalidEmailError,
    InvalidPasswordError,
    InvalidCredentialsError,
    UserInactiveError,
    InvalidTokenError,
    TokenExpiredError,
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=RegisterResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password",
)
async def register(
    request: RegisterRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> RegisterResponse:
    """Register a new user account."""
    try:
        dto = CreateUserDTO(
            email=request.email,
            password=request.password,
            full_name=request.full_name,
        )

        user_dto = auth_service.register_user(dto)

        # Generate tokens for the new user
        tokens = auth_service.login(request.email, request.password)

        return RegisterResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
            user={
                "id": user_dto.id,
                "email": user_dto.email,
                "full_name": user_dto.full_name,
                "is_active": user_dto.is_active,
                "is_verified": user_dto.is_verified,
                "created_at": user_dto.created_at.isoformat() if user_dto.created_at else None,
                "updated_at": user_dto.updated_at.isoformat() if user_dto.updated_at else None,
            }
        )

    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        )
    except (InvalidEmailError, InvalidPasswordError) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Login",
    description="Authenticate with email and password to receive access tokens",
)
async def login(
    request: LoginRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> TokenResponse:
    """Login with email and password."""
    try:
        tokens = auth_service.login(request.email, request.password)

        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"],
        )

    except InvalidCredentialsError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
    except UserInactiveError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )


@router.post(
    "/refresh-token",
    response_model=AccessTokenResponse,
    summary="Refresh access token",
    description="Get a new access token using a valid refresh token",
)
async def refresh_token(
    request: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> AccessTokenResponse:
    """Refresh access token."""
    try:
        tokens = auth_service.refresh_token(request.refresh_token)

        return AccessTokenResponse(
            access_token=tokens["access_token"],
            token_type=tokens["token_type"],
        )

    except (InvalidTokenError, TokenExpiredError) as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )
