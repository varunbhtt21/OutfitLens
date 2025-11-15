"""
Common API schemas for standardized responses.
"""

from typing import Any, Generic, TypeVar
from pydantic import BaseModel, Field

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper."""

    success: bool = Field(default=True, description="Indicates success")
    data: T = Field(..., description="Response data")
    message: str = Field(default="Operation successful", description="Success message")


class ErrorDetail(BaseModel):
    """Error detail structure."""

    code: str = Field(..., description="Error code")
    message: str = Field(..., description="Human-readable error message")
    details: dict[str, Any] | None = Field(
        default=None, description="Additional error details"
    )


class ErrorResponse(BaseModel):
    """Standard error response wrapper."""

    success: bool = Field(default=False, description="Indicates failure")
    error: ErrorDetail = Field(..., description="Error details")


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Health status")
    app: str = Field(..., description="Application name")
    environment: str = Field(..., description="Environment")
