"""
User API schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class UserResponse(BaseModel):
    """Response schema for user information."""

    id: str = Field(..., description="User's unique identifier")
    email: EmailStr = Field(..., description="User's email address")
    full_name: str | None = Field(None, description="User's full name")
    is_active: bool = Field(..., description="Whether user account is active")
    is_verified: bool = Field(..., description="Whether user's email is verified")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")


class UpdateUserRequest(BaseModel):
    """Request schema for updating user profile."""

    full_name: str | None = Field(None, max_length=255, description="User's full name")


class ChangePasswordRequest(BaseModel):
    """Request schema for changing password."""

    old_password: str = Field(..., description="Current password")
    new_password: str = Field(
        ..., min_length=8, max_length=128, description="New password"
    )


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str = Field(..., description="Response message")
