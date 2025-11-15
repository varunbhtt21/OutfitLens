"""
Generation Data Transfer Objects (DTOs).
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from app.application.dtos.image_dtos import ImageDTO


@dataclass
class CreateGenerationDTO:
    """DTO for creating a new generation request."""

    user_id: str
    user_photo_id: str
    clothing_photo_id: str


@dataclass
class GenerationDTO:
    """DTO for generation output."""

    id: str
    user_id: str
    status: str
    user_photo: ImageDTO
    clothing_photo: ImageDTO
    result_image: ImageDTO | None
    error_message: str | None
    processing_time_ms: int | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None


@dataclass
class GenerationStatusDTO:
    """DTO for generation status only."""

    id: str
    status: str
    error_message: str | None = None


@dataclass
class GenerationHistoryDTO:
    """DTO for generation history with pagination."""

    items: list[GenerationDTO]
    total: int
    page: int
    page_size: int
    has_more: bool
