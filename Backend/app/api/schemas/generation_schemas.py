"""
Generation API schemas for request/response validation.
"""

from datetime import datetime
from pydantic import BaseModel, Field

from app.api.schemas.image_schemas import ImageResponse


class CreateGenerationRequest(BaseModel):
    """Request schema for creating a generation."""

    user_photo_id: str = Field(..., description="ID of the user's photo")
    clothing_photo_id: str = Field(..., description="ID of the clothing item photo")


class GenerationResponse(BaseModel):
    """Response schema for generation information."""

    id: str = Field(..., description="Generation's unique identifier")
    user_id: str = Field(..., description="Owner's user ID")
    status: str = Field(..., description="Generation status")
    user_photo: ImageResponse = Field(..., description="User's photo")
    clothing_photo: ImageResponse = Field(..., description="Clothing item photo")
    result_image: ImageResponse | None = Field(
        None, description="Generated result image"
    )
    error_message: str | None = Field(None, description="Error message if failed")
    processing_time_ms: int | None = Field(
        None, description="Processing time in milliseconds"
    )
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: datetime | None = Field(None, description="Completion timestamp")


class GenerationStatusResponse(BaseModel):
    """Response schema for generation status."""

    id: str = Field(..., description="Generation's unique identifier")
    status: str = Field(..., description="Generation status")
    error_message: str | None = Field(None, description="Error message if failed")


class GenerationHistoryResponse(BaseModel):
    """Response schema for generation history with pagination."""

    items: list[GenerationResponse] = Field(..., description="List of generations")
    total: int = Field(..., description="Total number of generations")
    page: int = Field(..., description="Current page number")
    page_size: int = Field(..., description="Number of items per page")
    has_more: bool = Field(..., description="Whether there are more pages")
