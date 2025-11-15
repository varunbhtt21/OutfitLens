"""
Application configuration using Pydantic Settings.
Loads configuration from environment variables.
"""

from typing import List
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    APP_NAME: str = "OutfitLens"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # Database
    DATABASE_URL: str = "sqlite:///./outfitlens.db"

    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # File Storage
    STORAGE_PATH: str = "./storage"
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_IMAGE_FORMATS: str = "jpg,jpeg,png,webp"

    # Google Gemini AI
    GEMINI_API_KEY: str
    GEMINI_MODEL: str = "gemini-2.0-flash-exp"
    GEMINI_TIMEOUT_SECONDS: int = 30
    GEMINI_MAX_RETRIES: int = 3

    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"

    # Rate Limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_PER_MINUTE: int = 100
    AUTH_RATE_LIMIT_PER_MINUTE: int = 10

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @field_validator("SECRET_KEY")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate that SECRET_KEY is set and not empty."""
        if not v or len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v

    @field_validator("GEMINI_API_KEY")
    @classmethod
    def validate_gemini_api_key(cls, v: str) -> str:
        """Validate that GEMINI_API_KEY is set (warning only in development)."""
        if not v:
            raise ValueError("GEMINI_API_KEY must be set")
        # Allow placeholder in development, but warn
        if v == "your-gemini-api-key-here":
            import warnings
            warnings.warn(
                "GEMINI_API_KEY is set to placeholder value. "
                "AI generation will not work until you set a valid API key."
            )
        return v

    @property
    def allowed_image_formats_list(self) -> List[str]:
        """Get allowed image formats as a list."""
        return [fmt.strip().lower() for fmt in self.ALLOWED_IMAGE_FORMATS.split(",")]

    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]

    @property
    def max_upload_size_bytes(self) -> int:
        """Get max upload size in bytes."""
        return self.MAX_UPLOAD_SIZE_MB * 1024 * 1024


# Create settings instance
settings = Settings()
