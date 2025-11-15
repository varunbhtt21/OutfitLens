"""
User Data Transfer Objects (DTOs).
DTOs are used to transfer data between application layer and API layer.
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    """DTO for creating a new user."""

    email: str
    password: str
    full_name: str | None = None


@dataclass
class UserDTO:
    """DTO for user output."""

    id: str
    email: str
    full_name: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime


@dataclass
class UpdateUserDTO:
    """DTO for updating user profile."""

    full_name: str | None = None


@dataclass
class ChangePasswordDTO:
    """DTO for changing user password."""

    old_password: str
    new_password: str
