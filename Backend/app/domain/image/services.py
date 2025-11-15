"""
Image domain services.
"""

from typing import BinaryIO
from PIL import Image as PILImage

from app.domain.image.value_objects import ImageFormat, ImageDimensions, ImageSize
from app.domain.image.entities import ImageMetadata
from app.core.exceptions import InvalidImageFormatError, InvalidImageSizeError
from app.core.config import settings


class ImageDomainService:
    """
    Domain service for Image-related business logic.
    """

    def validate_image_format(self, filename: str) -> ImageFormat:
        """
        Validate image format from filename.

        Args:
            filename: Name of the file

        Returns:
            ImageFormat if valid

        Raises:
            InvalidImageFormatError: If format is not supported
        """
        extension = filename.rsplit(".", 1)[-1] if "." in filename else ""

        if not extension:
            raise InvalidImageFormatError("File has no extension")

        # Check if format is allowed
        allowed_formats = settings.allowed_image_formats_list
        if extension.lower() not in allowed_formats:
            raise InvalidImageFormatError(
                f"Format '{extension}' not allowed. Allowed formats: {', '.join(allowed_formats)}"
            )

        return ImageFormat(extension)

    def validate_image_size(self, file_size: int) -> ImageSize:
        """
        Validate image file size.

        Args:
            file_size: Size of file in bytes

        Returns:
            ImageSize if valid

        Raises:
            InvalidImageSizeError: If size exceeds maximum
        """
        return ImageSize(file_size)

    def extract_metadata(
        self, file: BinaryIO, filename: str, file_size: int
    ) -> ImageMetadata:
        """
        Extract metadata from an image file.

        Args:
            file: File-like object containing image data
            filename: Name of the file
            file_size: Size of file in bytes

        Returns:
            ImageMetadata object

        Raises:
            InvalidImageFormatError: If image cannot be processed
        """
        # Validate format and size
        image_format = self.validate_image_format(filename)
        image_size = self.validate_image_size(file_size)

        try:
            # Open image with Pillow to extract dimensions
            with PILImage.open(file) as img:
                width, height = img.size
                dimensions = ImageDimensions(width, height)
                mime_type = image_format.mime_type

            return ImageMetadata(
                file_size=image_size,
                dimensions=dimensions,
                format=image_format,
                mime_type=mime_type,
            )
        except Exception as e:
            raise InvalidImageFormatError(f"Failed to process image: {str(e)}")
