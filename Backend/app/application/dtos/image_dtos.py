"""
Image Data Transfer Objects (DTOs).
"""

from datetime import datetime
from dataclasses import dataclass


@dataclass
class UploadImageDTO:
    """DTO for image upload request."""

    user_id: str
    image_type: str  # "user_photo" or "clothing_photo"
    file_path: str
    file_size: int
    width: int
    height: int
    mime_type: str


@dataclass
class ImageDTO:
    """DTO for image output."""

    id: str
    user_id: str
    image_type: str
    file_path: str
    file_size: int
    mime_type: str
    width: int
    height: int
    created_at: datetime
    url: str | None = None


@dataclass
class ImageMetadataDTO:
    """DTO for image metadata."""

    file_size_bytes: int
    file_size_mb: float
    width: int
    height: int
    format: str
    mime_type: str
