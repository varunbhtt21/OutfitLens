"""
Generation domain entities.
"""

from datetime import datetime
from typing import Optional

from app.domain.shared.base import AggregateRoot
from app.domain.generation.value_objects import GenerationStatus, ProcessingTime
from app.domain.shared.events import (
    GenerationStartedEvent,
    GenerationCompletedEvent,
    GenerationFailedEvent,
)
from app.core.exceptions import InvalidGenerationStateError


class Generation(AggregateRoot):
    """
    Generation aggregate root.
    Represents an AI generation request and its lifecycle.
    """

    def __init__(
        self,
        user_id: str,
        user_photo_id: str,
        clothing_photo_id: str,
        status: GenerationStatus | None = None,
        result_image_id: str | None = None,
        error_message: str | None = None,
        processing_time: ProcessingTime | None = None,
        id: str | None = None,
        created_at: datetime | None = None,
        updated_at: datetime | None = None,
        completed_at: datetime | None = None,
    ):
        """
        Create a Generation entity.

        Args:
            user_id: ID of the user who requested the generation
            user_photo_id: ID of the user's photo
            clothing_photo_id: ID of the clothing photo
            status: Current status of the generation
            result_image_id: ID of the generated result image
            error_message: Error message if generation failed
            processing_time: Time taken to process the generation
            id: Unique identifier (generates if not provided)
            created_at: Creation timestamp
            updated_at: Last update timestamp
            completed_at: Completion timestamp
        """
        super().__init__(id)

        self.user_id = user_id
        self.user_photo_id = user_photo_id
        self.clothing_photo_id = clothing_photo_id
        self.status = status or GenerationStatus("pending")
        self.result_image_id = result_image_id
        self.error_message = error_message
        self.processing_time = processing_time
        self.completed_at = completed_at

        if created_at:
            self.created_at = created_at
        if updated_at:
            self.updated_at = updated_at

    @staticmethod
    def create(
        user_id: str, user_photo_id: str, clothing_photo_id: str
    ) -> "Generation":
        """
        Factory method to create a new generation request.

        Args:
            user_id: ID of the user requesting generation
            user_photo_id: ID of user's photo
            clothing_photo_id: ID of clothing photo

        Returns:
            New Generation instance with pending status
        """
        generation = Generation(
            user_id=user_id,
            user_photo_id=user_photo_id,
            clothing_photo_id=clothing_photo_id,
            status=GenerationStatus("pending"),
        )

        return generation

    def start_processing(self) -> None:
        """
        Mark generation as processing.

        Raises:
            InvalidGenerationStateError: If status transition is invalid
        """
        new_status = GenerationStatus("processing")

        if not self.status.can_transition_to(new_status):
            raise InvalidGenerationStateError(
                f"Cannot transition from {self.status} to {new_status}"
            )

        self.status = new_status
        self.update_timestamp()

        # Add domain event
        self.add_domain_event(GenerationStartedEvent.create(self.id, self.user_id))

    def complete(self, result_image_id: str, processing_time_ms: int) -> None:
        """
        Mark generation as completed successfully.

        Args:
            result_image_id: ID of the generated result image
            processing_time_ms: Processing time in milliseconds

        Raises:
            InvalidGenerationStateError: If status transition is invalid
        """
        new_status = GenerationStatus("completed")

        if not self.status.can_transition_to(new_status):
            raise InvalidGenerationStateError(
                f"Cannot transition from {self.status} to {new_status}"
            )

        self.status = new_status
        self.result_image_id = result_image_id
        self.processing_time = ProcessingTime(processing_time_ms)
        self.completed_at = datetime.utcnow()
        self.update_timestamp()

        # Add domain event
        self.add_domain_event(
            GenerationCompletedEvent.create(
                self.id, self.user_id, processing_time_ms
            )
        )

    def fail(self, error_message: str) -> None:
        """
        Mark generation as failed.

        Args:
            error_message: Error message describing the failure

        Raises:
            InvalidGenerationStateError: If status transition is invalid
        """
        new_status = GenerationStatus("failed")

        if not self.status.can_transition_to(new_status):
            raise InvalidGenerationStateError(
                f"Cannot transition from {self.status} to {new_status}"
            )

        self.status = new_status
        self.error_message = error_message
        self.completed_at = datetime.utcnow()
        self.update_timestamp()

        # Add domain event
        self.add_domain_event(
            GenerationFailedEvent.create(self.id, self.user_id, error_message)
        )

    def belongs_to_user(self, user_id: str) -> bool:
        """
        Check if generation belongs to a specific user.

        Args:
            user_id: User ID to check

        Returns:
            True if generation belongs to user, False otherwise
        """
        return self.user_id == user_id

    def is_ready_for_processing(self) -> bool:
        """
        Check if generation is ready to be processed.

        Returns:
            True if status is pending, False otherwise
        """
        return self.status.is_pending()

    def is_complete(self) -> bool:
        """
        Check if generation is complete (successfully or failed).

        Returns:
            True if status is terminal, False otherwise
        """
        return self.status.is_terminal()

    def __repr__(self) -> str:
        """String representation."""
        return (
            f"Generation(id={self.id!r}, status={self.status}, "
            f"user_id={self.user_id!r})"
        )
