"""
Value objects for the Generation domain.
"""

from app.domain.shared.base import ValueObject
from app.domain.shared.enums import GenerationStatusEnum
from app.core.exceptions import InvalidGenerationStateError


class GenerationStatus(ValueObject):
    """Generation status value object."""

    def __init__(self, value: str):
        """
        Create GenerationStatus value object.

        Args:
            value: Status string

        Raises:
            ValueError: If status is not valid
        """
        try:
            self.value = GenerationStatusEnum(value)
        except ValueError:
            raise ValueError(f"Invalid generation status: {value}")

    def is_pending(self) -> bool:
        """Check if status is pending."""
        return self.value == GenerationStatusEnum.PENDING

    def is_processing(self) -> bool:
        """Check if status is processing."""
        return self.value == GenerationStatusEnum.PROCESSING

    def is_completed(self) -> bool:
        """Check if status is completed."""
        return self.value == GenerationStatusEnum.COMPLETED

    def is_failed(self) -> bool:
        """Check if status is failed."""
        return self.value == GenerationStatusEnum.FAILED

    def is_terminal(self) -> bool:
        """Check if status is terminal (completed or failed)."""
        return self.is_completed() or self.is_failed()

    def can_transition_to(self, new_status: "GenerationStatus") -> bool:
        """
        Check if transition to new status is valid.

        Valid transitions:
        - pending -> processing
        - processing -> completed
        - processing -> failed
        - Any terminal state can't transition

        Args:
            new_status: Status to transition to

        Returns:
            True if transition is valid, False otherwise
        """
        if self.is_terminal():
            return False

        valid_transitions = {
            GenerationStatusEnum.PENDING: [GenerationStatusEnum.PROCESSING],
            GenerationStatusEnum.PROCESSING: [
                GenerationStatusEnum.COMPLETED,
                GenerationStatusEnum.FAILED,
            ],
        }

        return new_status.value in valid_transitions.get(self.value, [])

    def __str__(self) -> str:
        """String representation."""
        return self.value.value


class ProcessingTime(ValueObject):
    """Processing time value object (in milliseconds)."""

    def __init__(self, milliseconds: int):
        """
        Create ProcessingTime value object.

        Args:
            milliseconds: Processing time in milliseconds

        Raises:
            ValueError: If time is negative
        """
        if milliseconds < 0:
            raise ValueError("Processing time cannot be negative")

        if milliseconds > 300000:  # 5 minutes max
            raise ValueError("Processing time is unreasonably high (max 5 minutes)")

        self.milliseconds = milliseconds

    @property
    def seconds(self) -> float:
        """Get processing time in seconds."""
        return self.milliseconds / 1000

    @property
    def minutes(self) -> float:
        """Get processing time in minutes."""
        return self.milliseconds / 60000

    def is_fast(self) -> bool:
        """Check if processing was fast (< 5 seconds)."""
        return self.milliseconds < 5000

    def is_slow(self) -> bool:
        """Check if processing was slow (> 15 seconds)."""
        return self.milliseconds > 15000

    def __str__(self) -> str:
        """String representation."""
        if self.milliseconds < 1000:
            return f"{self.milliseconds}ms"
        else:
            return f"{self.seconds:.2f}s"
