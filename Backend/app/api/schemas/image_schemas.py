"""
Image API schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field


class ImageResponse(BaseModel):
    """Response schema for image information."""

    id: str = Field(..., description="Image's unique identifier")
    user_id: str = Field(..., description="Owner's user ID")
    image_type: str = Field(..., description="Type of image")
    file_path: str = Field(..., description="File path")
    file_size: int = Field(..., description="File size in bytes")
    mime_type: str = Field(..., description="MIME type")
    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")
    created_at: datetime = Field(..., description="Upload timestamp")
    url: str | None = Field(None, description="URL to access the image")


class UploadImageResponse(BaseModel):
    """Response schema for image upload."""

    id: str = Field(..., description="Image's unique identifier")
    image_type: str = Field(..., description="Type of image")
    file_size: int = Field(..., description="File size in bytes")
    width: int = Field(..., description="Image width in pixels")
    height: int = Field(..., description="Image height in pixels")
    url: str | None = Field(None, description="URL to access the image")
    message: str = Field(default="Image uploaded successfully")


class ImageListResponse(BaseModel):
    """Response schema for list of images."""

    images: list[ImageResponse] = Field(..., description="List of images")
    total: int = Field(..., description="Total number of images")
