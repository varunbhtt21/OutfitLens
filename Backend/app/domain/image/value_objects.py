"""
Value objects for the Image domain.
"""

from app.domain.shared.base import ValueObject
from app.domain.shared.enums import ImageFormatEnum, ImageTypeEnum
from app.core.exceptions import InvalidImageFormatError, InvalidImageSizeError
from app.core.config import settings


class ImageFormat(ValueObject):
    """Image format value object with validation."""

    def __init__(self, value: str):
        """
        Create an ImageFormat value object.

        Args:
            value: Image format string (e.g., "jpg", "png")

        Raises:
            InvalidImageFormatError: If format is not supported
        """
        try:
            self.value = ImageFormatEnum.from_extension(value)
        except ValueError as e:
            raise InvalidImageFormatError(str(e))

    @property
    def extension(self) -> str:
        """Get file extension."""
        return self.value.value

    @property
    def mime_type(self) -> str:
        """Get MIME type."""
        return self.value.to_mime_type()

    def __str__(self) -> str:
        """String representation."""
        return self.value.value


class ImageDimensions(ValueObject):
    """Image dimensions value object."""

    def __init__(self, width: int, height: int):
        """
        Create ImageDimensions value object.

        Args:
            width: Image width in pixels
            height: Image height in pixels

        Raises:
            ValueError: If dimensions are invalid
        """
        if width <= 0 or height <= 0:
            raise ValueError("Image dimensions must be positive")

        if width > 10000 or height > 10000:
            raise ValueError("Image dimensions are too large (max 10000x10000)")

        self.width = width
        self.height = height

    @property
    def aspect_ratio(self) -> float:
        """Calculate aspect ratio."""
        return self.width / self.height

    @property
    def total_pixels(self) -> int:
        """Calculate total number of pixels."""
        return self.width * self.height

    def __str__(self) -> str:
        """String representation."""
        return f"{self.width}x{self.height}"


class ImageSize(ValueObject):
    """Image file size value object with validation."""

    def __init__(self, size_bytes: int):
        """
        Create ImageSize value object.

        Args:
            size_bytes: File size in bytes

        Raises:
            InvalidImageSizeError: If size exceeds maximum allowed
        """
        if size_bytes <= 0:
            raise ValueError("Image size must be positive")

        max_size_bytes = settings.max_upload_size_bytes
        if size_bytes > max_size_bytes:
            raise InvalidImageSizeError(
                f"Image size ({self._format_size(size_bytes)}) exceeds maximum allowed "
                f"({self._format_size(max_size_bytes)})"
            )

        self.size_bytes = size_bytes

    @property
    def size_kb(self) -> float:
        """Get size in kilobytes."""
        return self.size_bytes / 1024

    @property
    def size_mb(self) -> float:
        """Get size in megabytes."""
        return self.size_bytes / (1024 * 1024)

    @staticmethod
    def _format_size(size_bytes: int) -> str:
        """Format size in human-readable format."""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.2f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.2f} MB"

    def __str__(self) -> str:
        """String representation."""
        return self._format_size(self.size_bytes)


class ImageType(ValueObject):
    """Image type value object."""

    def __init__(self, value: str):
        """
        Create ImageType value object.

        Args:
            value: Image type string

        Raises:
            ValueError: If type is not valid
        """
        try:
            self.value = ImageTypeEnum(value)
        except ValueError:
            raise ValueError(f"Invalid image type: {value}")

    def is_user_photo(self) -> bool:
        """Check if this is a user photo."""
        return self.value == ImageTypeEnum.USER_PHOTO

    def is_clothing_photo(self) -> bool:
        """Check if this is a clothing photo."""
        return self.value == ImageTypeEnum.CLOTHING_PHOTO

    def is_generated_result(self) -> bool:
        """Check if this is a generated result."""
        return self.value == ImageTypeEnum.GENERATED_RESULT

    def __str__(self) -> str:
        """String representation."""
        return self.value.value
