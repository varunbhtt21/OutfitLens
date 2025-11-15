"""
Domain events for the application.
Domain events represent things that have happened in the domain.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass(frozen=True)
class DomainEvent:
    """
    Base class for all domain events.
    Domain events are immutable records of something that happened.
    """

    occurred_at: datetime
    aggregate_id: str
    event_data: dict[str, Any]

    def __post_init__(self) -> None:
        """Validate event after initialization."""
        if not self.aggregate_id:
            raise ValueError("aggregate_id cannot be empty")


@dataclass(frozen=True)
class UserRegisteredEvent(DomainEvent):
    """Event raised when a new user registers."""

    @staticmethod
    def create(user_id: str, email: str) -> "UserRegisteredEvent":
        """
        Create a UserRegisteredEvent.

        Args:
            user_id: ID of the registered user
            email: Email of the registered user

        Returns:
            UserRegisteredEvent instance
        """
        return UserRegisteredEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=user_id,
            event_data={"email": email},
        )


@dataclass(frozen=True)
class UserVerifiedEvent(DomainEvent):
    """Event raised when a user's email is verified."""

    @staticmethod
    def create(user_id: str) -> "UserVerifiedEvent":
        """
        Create a UserVerifiedEvent.

        Args:
            user_id: ID of the verified user

        Returns:
            UserVerifiedEvent instance
        """
        return UserVerifiedEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=user_id,
            event_data={},
        )


@dataclass(frozen=True)
class ImageUploadedEvent(DomainEvent):
    """Event raised when an image is uploaded."""

    @staticmethod
    def create(image_id: str, user_id: str, image_type: str) -> "ImageUploadedEvent":
        """
        Create an ImageUploadedEvent.

        Args:
            image_id: ID of the uploaded image
            user_id: ID of the user who uploaded the image
            image_type: Type of image uploaded

        Returns:
            ImageUploadedEvent instance
        """
        return ImageUploadedEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=image_id,
            event_data={"user_id": user_id, "image_type": image_type},
        )


@dataclass(frozen=True)
class GenerationStartedEvent(DomainEvent):
    """Event raised when a generation starts processing."""

    @staticmethod
    def create(generation_id: str, user_id: str) -> "GenerationStartedEvent":
        """
        Create a GenerationStartedEvent.

        Args:
            generation_id: ID of the generation
            user_id: ID of the user who requested the generation

        Returns:
            GenerationStartedEvent instance
        """
        return GenerationStartedEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=generation_id,
            event_data={"user_id": user_id},
        )


@dataclass(frozen=True)
class GenerationCompletedEvent(DomainEvent):
    """Event raised when a generation completes successfully."""

    @staticmethod
    def create(
        generation_id: str, user_id: str, processing_time_ms: int
    ) -> "GenerationCompletedEvent":
        """
        Create a GenerationCompletedEvent.

        Args:
            generation_id: ID of the generation
            user_id: ID of the user
            processing_time_ms: Time taken to process in milliseconds

        Returns:
            GenerationCompletedEvent instance
        """
        return GenerationCompletedEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=generation_id,
            event_data={"user_id": user_id, "processing_time_ms": processing_time_ms},
        )


@dataclass(frozen=True)
class GenerationFailedEvent(DomainEvent):
    """Event raised when a generation fails."""

    @staticmethod
    def create(generation_id: str, user_id: str, error_message: str) -> "GenerationFailedEvent":
        """
        Create a GenerationFailedEvent.

        Args:
            generation_id: ID of the generation
            user_id: ID of the user
            error_message: Error message describing the failure

        Returns:
            GenerationFailedEvent instance
        """
        return GenerationFailedEvent(
            occurred_at=datetime.utcnow(),
            aggregate_id=generation_id,
            event_data={"user_id": user_id, "error_message": error_message},
        )
