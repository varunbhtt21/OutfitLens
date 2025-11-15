"""
Generation repository interface.
"""

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.generation.entities import Generation


class GenerationRepository(ABC):
    """
    Repository interface for Generation aggregate.
    Infrastructure layer will implement this interface.
    """

    @abstractmethod
    def create(self, generation: Generation) -> Generation:
        """
        Create a new generation.

        Args:
            generation: Generation entity to persist

        Returns:
            Created generation entity

        Raises:
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    def get_by_id(self, generation_id: str) -> Optional[Generation]:
        """
        Get generation by ID.

        Args:
            generation_id: Generation's unique identifier

        Returns:
            Generation entity if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_user(
        self, user_id: str, limit: int = 20, offset: int = 0
    ) -> List[Generation]:
        """
        Get all generations for a user with pagination.

        Args:
            user_id: User's unique identifier
            limit: Maximum number of results to return
            offset: Number of results to skip

        Returns:
            List of Generation entities ordered by created_at desc
        """
        pass

    @abstractmethod
    def update(self, generation: Generation) -> Generation:
        """
        Update an existing generation.

        Args:
            generation: Generation entity with updated values

        Returns:
            Updated generation entity

        Raises:
            GenerationNotFoundError: If generation doesn't exist
            DatabaseError: If database operation fails
        """
        pass

    @abstractmethod
    def delete(self, generation_id: str) -> bool:
        """
        Delete a generation by ID.

        Args:
            generation_id: Generation's unique identifier

        Returns:
            True if deleted, False if generation not found
        """
        pass

    @abstractmethod
    def count_by_user(self, user_id: str) -> int:
        """
        Count total generations for a user.

        Args:
            user_id: User's unique identifier

        Returns:
            Total count of generations
        """
        pass
