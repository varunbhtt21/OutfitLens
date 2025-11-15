"""
FastAPI dependency injection.
Provides database sessions, services, and authentication.
"""

from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.database.repositories.user_repository import UserRepositoryImpl
from app.infrastructure.database.repositories.image_repository import ImageRepositoryImpl
from app.infrastructure.database.repositories.generation_repository import (
    GenerationRepositoryImpl,
)
from app.infrastructure.storage.local_storage import LocalStorageService
from app.infrastructure.external.gemini_service import GeminiService
from app.domain.user.services import UserDomainService
from app.domain.image.services import ImageDomainService
from app.domain.generation.services import GenerationDomainService
from app.application.services.auth_service import AuthService
from app.application.services.user_service import UserService
from app.application.services.image_service import ImageService
from app.application.services.generation_service import GenerationService
from app.core.security import get_user_id_from_token
from app.core.exceptions import InvalidTokenError, TokenExpiredError, UserNotFoundError

# Security scheme for JWT Bearer tokens
security = HTTPBearer()


# Database dependency
def get_database() -> Session:
    """Get database session."""
    return next(get_db())


# Repository dependencies
def get_user_repository(db: Session = Depends(get_database)) -> UserRepositoryImpl:
    """Get user repository instance."""
    return UserRepositoryImpl(db)


def get_image_repository(db: Session = Depends(get_database)) -> ImageRepositoryImpl:
    """Get image repository instance."""
    return ImageRepositoryImpl(db)


def get_generation_repository(
    db: Session = Depends(get_database),
) -> GenerationRepositoryImpl:
    """Get generation repository instance."""
    return GenerationRepositoryImpl(db)


# Storage dependency
def get_storage_service() -> LocalStorageService:
    """Get storage service instance."""
    return LocalStorageService()


# External service dependencies
def get_gemini_service() -> GeminiService:
    """Get Gemini AI service instance."""
    return GeminiService()


# Domain service dependencies
def get_user_domain_service(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
) -> UserDomainService:
    """Get user domain service instance."""
    return UserDomainService(user_repository)


def get_image_domain_service() -> ImageDomainService:
    """Get image domain service instance."""
    return ImageDomainService()


def get_generation_domain_service(
    generation_repository: GenerationRepositoryImpl = Depends(get_generation_repository),
    image_repository: ImageRepositoryImpl = Depends(get_image_repository),
) -> GenerationDomainService:
    """Get generation domain service instance."""
    return GenerationDomainService(generation_repository, image_repository)


# Application service dependencies
def get_auth_service(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    user_domain_service: UserDomainService = Depends(get_user_domain_service),
) -> AuthService:
    """Get authentication service instance."""
    return AuthService(user_repository, user_domain_service)


def get_user_service(
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
    user_domain_service: UserDomainService = Depends(get_user_domain_service),
) -> UserService:
    """Get user service instance."""
    return UserService(user_repository, user_domain_service)


def get_image_service(
    image_repository: ImageRepositoryImpl = Depends(get_image_repository),
    storage_service: LocalStorageService = Depends(get_storage_service),
    image_domain_service: ImageDomainService = Depends(get_image_domain_service),
) -> ImageService:
    """Get image service instance."""
    return ImageService(image_repository, storage_service, image_domain_service)


def get_generation_service(
    generation_repository: GenerationRepositoryImpl = Depends(get_generation_repository),
    image_repository: ImageRepositoryImpl = Depends(get_image_repository),
    gemini_service: GeminiService = Depends(get_gemini_service),
    storage_service: LocalStorageService = Depends(get_storage_service),
    generation_domain_service: GenerationDomainService = Depends(
        get_generation_domain_service
    ),
) -> GenerationService:
    """Get generation service instance."""
    return GenerationService(
        generation_repository,
        image_repository,
        gemini_service,
        storage_service,
        generation_domain_service,
    )


# Authentication dependency
async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
) -> str:
    """
    Get current authenticated user ID from JWT token.

    Args:
        credentials: HTTP Bearer credentials with JWT token
        user_repository: User repository to verify user exists

    Returns:
        User ID string

    Raises:
        HTTPException: If authentication fails
    """
    try:
        # Extract token
        token = credentials.credentials

        # Get user ID from token
        user_id = get_user_id_from_token(token)

        # Verify user exists and is active
        user = user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user_id

    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Type alias for authenticated user dependency
CurrentUser = Annotated[str, Depends(get_current_user)]
