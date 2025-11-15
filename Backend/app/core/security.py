"""
Security utilities for password hashing and JWT token management.
"""

from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.core.exceptions import InvalidTokenError, TokenExpiredError

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# =============================================================================
# Password Hashing
# =============================================================================


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        Hashed password
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


# =============================================================================
# JWT Token Management
# =============================================================================


def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token.

    Args:
        data: Data to encode in the token (usually {"sub": user_id})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT refresh token.

    Args:
        data: Data to encode in the token (usually {"sub": user_id})
        expires_delta: Optional custom expiration time

    Returns:
        Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    """
    Decode and validate a JWT token.

    Args:
        token: JWT token to decode

    Returns:
        Decoded token payload

    Raises:
        TokenExpiredError: If token has expired
        InvalidTokenError: If token is invalid
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired")
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")


def verify_token_type(payload: dict[str, Any], expected_type: str) -> bool:
    """
    Verify that the token is of the expected type (access or refresh).

    Args:
        payload: Decoded token payload
        expected_type: Expected token type ("access" or "refresh")

    Returns:
        True if token type matches, False otherwise
    """
    token_type = payload.get("type")
    return token_type == expected_type


def get_user_id_from_token(token: str) -> str:
    """
    Extract user ID from a JWT token.

    Args:
        token: JWT token

    Returns:
        User ID from token

    Raises:
        InvalidTokenError: If token is invalid or doesn't contain user ID
    """
    payload = decode_token(token)
    user_id: str | None = payload.get("sub")

    if user_id is None:
        raise InvalidTokenError("Token does not contain user ID")

    return user_id
