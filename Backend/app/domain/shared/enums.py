"""
Shared enumerations used across multiple domains.
"""

from enum import Enum


class ImageTypeEnum(str, Enum):
    """Types of images in the system."""

    USER_PHOTO = "user_photo"
    CLOTHING_PHOTO = "clothing_photo"
    GENERATED_RESULT = "generated_result"


class GenerationStatusEnum(str, Enum):
    """Status of generation requests."""

    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ImageFormatEnum(str, Enum):
    """Supported image formats."""

    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"
    WEBP = "webp"

    @classmethod
    def from_mime_type(cls, mime_type: str) -> "ImageFormatEnum":
        """
        Get image format from MIME type.

        Args:
            mime_type: MIME type string (e.g., "image/jpeg")

        Returns:
            ImageFormatEnum value

        Raises:
            ValueError: If MIME type is not supported
        """
        mime_to_format = {
            "image/jpeg": cls.JPEG,
            "image/jpg": cls.JPG,
            "image/png": cls.PNG,
            "image/webp": cls.WEBP,
        }

        format_enum = mime_to_format.get(mime_type.lower())
        if not format_enum:
            raise ValueError(f"Unsupported MIME type: {mime_type}")

        return format_enum

    @classmethod
    def from_extension(cls, extension: str) -> "ImageFormatEnum":
        """
        Get image format from file extension.

        Args:
            extension: File extension (e.g., "jpg", ".jpg")

        Returns:
            ImageFormatEnum value

        Raises:
            ValueError: If extension is not supported
        """
        # Remove leading dot if present
        ext = extension.lstrip(".").lower()

        try:
            return cls(ext)
        except ValueError:
            raise ValueError(f"Unsupported image format: {extension}")

    def to_mime_type(self) -> str:
        """
        Convert format to MIME type.

        Returns:
            MIME type string
        """
        format_to_mime = {
            self.JPG: "image/jpeg",
            self.JPEG: "image/jpeg",
            self.PNG: "image/png",
            self.WEBP: "image/webp",
        }
        return format_to_mime[self]
