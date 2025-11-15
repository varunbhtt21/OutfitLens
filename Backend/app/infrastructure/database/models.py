"""
SQLAlchemy ORM models for database tables.
These are infrastructure-layer implementations of domain entities.
"""

import uuid
from datetime import datetime
from typing import List

from sqlalchemy import String, Boolean, Integer, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.connection import Base


# Helper function to generate UUIDs
def generate_uuid() -> str:
    """Generate a UUID string."""
    return str(uuid.uuid4())


class UserModel(Base):
    """
    User table model.
    Represents a user account with authentication credentials.
    """

    __tablename__ = "users"

    # Primary key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # User credentials
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # User profile
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # User status
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    images: Mapped[List["ImageModel"]] = relationship(
        "ImageModel", back_populates="user", cascade="all, delete-orphan"
    )
    generations: Mapped[List["GenerationModel"]] = relationship(
        "GenerationModel", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class ImageModel(Base):
    """
    Image table model.
    Represents uploaded images (user photos, clothing photos, generated results).
    """

    __tablename__ = "images"

    # Primary key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Image type (user_photo, clothing_photo, generated_result)
    image_type: Mapped[str] = mapped_column(String(50), nullable=False)

    # File information
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    file_size: Mapped[int | None] = mapped_column(Integer, nullable=True)
    mime_type: Mapped[str | None] = mapped_column(String(50), nullable=True)

    # Image dimensions
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Timestamp
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )

    # Relationships
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="images")

    def __repr__(self) -> str:
        return f"<Image(id={self.id}, type={self.image_type}, user_id={self.user_id})>"


class GenerationModel(Base):
    """
    Generation table model.
    Represents AI generation requests and their results.
    """

    __tablename__ = "generations"

    # Primary key
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=generate_uuid)

    # Foreign key to user
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Foreign keys to images
    user_photo_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("images.id"), nullable=False
    )
    clothing_photo_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("images.id"), nullable=False
    )
    result_image_id: Mapped[str | None] = mapped_column(
        String(36), ForeignKey("images.id"), nullable=True
    )

    # Generation status (pending, processing, completed, failed)
    status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending", index=True
    )

    # Error information (if generation failed)
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Processing time in milliseconds
    processing_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # Relationships
    user: Mapped["UserModel"] = relationship("UserModel", back_populates="generations")
    user_photo: Mapped["ImageModel"] = relationship(
        "ImageModel", foreign_keys=[user_photo_id], lazy="joined"
    )
    clothing_photo: Mapped["ImageModel"] = relationship(
        "ImageModel", foreign_keys=[clothing_photo_id], lazy="joined"
    )
    result_image: Mapped["ImageModel | None"] = relationship(
        "ImageModel", foreign_keys=[result_image_id], lazy="joined"
    )

    def __repr__(self) -> str:
        return f"<Generation(id={self.id}, status={self.status}, user_id={self.user_id})>"
