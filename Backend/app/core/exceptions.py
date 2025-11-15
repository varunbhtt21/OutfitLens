"""
Custom exception hierarchy for the application.
Organized by layer: Domain, Application, Infrastructure.
"""


# =============================================================================
# Base Exceptions
# =============================================================================


class OutfitLensException(Exception):
    """Base exception for all OutfitLens exceptions."""

    def __init__(self, message: str, details: dict | None = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


# =============================================================================
# Domain Layer Exceptions
# =============================================================================


class DomainException(OutfitLensException):
    """Base exception for domain layer."""

    pass


class UserAlreadyExistsError(DomainException):
    """Raised when attempting to create a user that already exists."""

    pass


class UserNotFoundError(DomainException):
    """Raised when a user is not found."""

    pass


class InvalidEmailError(DomainException):
    """Raised when email format is invalid."""

    pass


class InvalidPasswordError(DomainException):
    """Raised when password doesn't meet strength requirements."""

    pass


class InvalidImageFormatError(DomainException):
    """Raised when image format is not supported."""

    pass


class InvalidImageSizeError(DomainException):
    """Raised when image size exceeds maximum allowed."""

    pass


class ImageNotFoundError(DomainException):
    """Raised when an image is not found."""

    pass


class GenerationNotFoundError(DomainException):
    """Raised when a generation is not found."""

    pass


class GenerationFailedError(DomainException):
    """Raised when AI generation fails."""

    pass


class InvalidGenerationStateError(DomainException):
    """Raised when attempting invalid state transition for generation."""

    pass


# =============================================================================
# Application Layer Exceptions
# =============================================================================


class ApplicationException(OutfitLensException):
    """Base exception for application layer."""

    pass


class AuthenticationError(ApplicationException):
    """Raised when authentication fails."""

    pass


class AuthorizationError(ApplicationException):
    """Raised when user doesn't have permission for an operation."""

    pass


class InvalidCredentialsError(AuthenticationError):
    """Raised when login credentials are invalid."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when JWT token has expired."""

    pass


class InvalidTokenError(AuthenticationError):
    """Raised when JWT token is invalid."""

    pass


class UserNotVerifiedError(AuthorizationError):
    """Raised when user email is not verified."""

    pass


class UserInactiveError(AuthorizationError):
    """Raised when user account is inactive."""

    pass


class ResourceNotFoundError(ApplicationException):
    """Raised when a requested resource is not found."""

    pass


class ValidationError(ApplicationException):
    """Raised when input validation fails."""

    pass


# =============================================================================
# Infrastructure Layer Exceptions
# =============================================================================


class InfrastructureException(OutfitLensException):
    """Base exception for infrastructure layer."""

    pass


class DatabaseError(InfrastructureException):
    """Raised when a database operation fails."""

    pass


class StorageError(InfrastructureException):
    """Raised when a file storage operation fails."""

    pass


class FileNotFoundError(StorageError):
    """Raised when a file is not found in storage."""

    pass


class FileSaveError(StorageError):
    """Raised when file save operation fails."""

    pass


class FileDeleteError(StorageError):
    """Raised when file delete operation fails."""

    pass


class ExternalServiceError(InfrastructureException):
    """Raised when external service call fails."""

    pass


class GeminiAPIError(ExternalServiceError):
    """Raised when Gemini API call fails."""

    pass


class GeminiAPITimeoutError(GeminiAPIError):
    """Raised when Gemini API call times out."""

    pass


class GeminiAPIRateLimitError(GeminiAPIError):
    """Raised when Gemini API rate limit is exceeded."""

    pass


# =============================================================================
# HTTP Exceptions (for API layer)
# =============================================================================


class HTTPException(OutfitLensException):
    """Base HTTP exception with status code."""

    def __init__(
        self, status_code: int, message: str, details: dict | None = None
    ):
        self.status_code = status_code
        super().__init__(message, details)


class BadRequestError(HTTPException):
    """400 Bad Request."""

    def __init__(self, message: str = "Bad request", details: dict | None = None):
        super().__init__(400, message, details)


class UnauthorizedError(HTTPException):
    """401 Unauthorized."""

    def __init__(
        self, message: str = "Unauthorized", details: dict | None = None
    ):
        super().__init__(401, message, details)


class ForbiddenError(HTTPException):
    """403 Forbidden."""

    def __init__(self, message: str = "Forbidden", details: dict | None = None):
        super().__init__(403, message, details)


class NotFoundError(HTTPException):
    """404 Not Found."""

    def __init__(self, message: str = "Not found", details: dict | None = None):
        super().__init__(404, message, details)


class TooManyRequestsError(HTTPException):
    """429 Too Many Requests."""

    def __init__(
        self, message: str = "Too many requests", details: dict | None = None
    ):
        super().__init__(429, message, details)


class InternalServerError(HTTPException):
    """500 Internal Server Error."""

    def __init__(
        self, message: str = "Internal server error", details: dict | None = None
    ):
        super().__init__(500, message, details)


class ServiceUnavailableError(HTTPException):
    """503 Service Unavailable."""

    def __init__(
        self, message: str = "Service unavailable", details: dict | None = None
    ):
        super().__init__(503, message, details)
