"""
Base classes for domain entities, value objects, and aggregate roots.
These provide common functionality for all domain objects.
"""

from abc import ABC
from datetime import datetime
from typing import Any
import uuid


class ValueObject(ABC):
    """
    Base class for value objects.
    Value objects are immutable and compared by value, not identity.
    """

    def __eq__(self, other: Any) -> bool:
        """Compare value objects by their attributes."""
        if not isinstance(other, self.__class__):
            return False
        return self.__dict__ == other.__dict__

    def __hash__(self) -> int:
        """Hash based on attribute values."""
        return hash(tuple(sorted(self.__dict__.items())))

    def __repr__(self) -> str:
        """String representation of value object."""
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class Entity(ABC):
    """
    Base class for domain entities.
    Entities have identity and are compared by ID, not attributes.
    """

    def __init__(self, id: str | None = None):
        """
        Initialize entity with optional ID.

        Args:
            id: Unique identifier for the entity (generates UUID if not provided)
        """
        self.id: str = id or str(uuid.uuid4())
        self.created_at: datetime = datetime.utcnow()
        self.updated_at: datetime = datetime.utcnow()

    def __eq__(self, other: Any) -> bool:
        """Entities are equal if they have the same ID."""
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self) -> int:
        """Hash based on ID."""
        return hash(self.id)

    def __repr__(self) -> str:
        """String representation of entity."""
        return f"{self.__class__.__name__}(id={self.id!r})"

    def update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.utcnow()


class AggregateRoot(Entity):
    """
    Base class for aggregate roots.
    Aggregate roots are entities that serve as entry points to an aggregate.
    They maintain consistency boundaries and enforce invariants.
    """

    def __init__(self, id: str | None = None):
        """
        Initialize aggregate root.

        Args:
            id: Unique identifier for the aggregate root
        """
        super().__init__(id)
        self._domain_events: list[Any] = []

    def add_domain_event(self, event: Any) -> None:
        """
        Add a domain event to be published.

        Args:
            event: Domain event to add
        """
        self._domain_events.append(event)

    def clear_domain_events(self) -> None:
        """Clear all domain events."""
        self._domain_events.clear()

    def get_domain_events(self) -> list[Any]:
        """
        Get all domain events.

        Returns:
            List of domain events
        """
        return self._domain_events.copy()
