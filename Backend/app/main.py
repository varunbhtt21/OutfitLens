"""
FastAPI application entry point.
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.core.config import settings
from app.core.exceptions import (
    OutfitLensException,
    DomainException,
    ApplicationException,
    InfrastructureException,
    HTTPException as CustomHTTPException,
)
from app.api.routers import auth, users, images, generations
from app.api.schemas.common import HealthCheckResponse

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="OutfitLens - AI-powered virtual try-on application",
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(DomainException)
async def domain_exception_handler(request: Request, exc: DomainException):
    """Handle domain layer exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


@app.exception_handler(ApplicationException)
async def application_exception_handler(request: Request, exc: ApplicationException):
    """Handle application layer exceptions."""
    status_code = status.HTTP_400_BAD_REQUEST

    # Map specific exceptions to appropriate status codes
    if "Authentication" in exc.__class__.__name__:
        status_code = status.HTTP_401_UNAUTHORIZED
    elif "Authorization" in exc.__class__.__name__:
        status_code = status.HTTP_403_FORBIDDEN
    elif "NotFound" in exc.__class__.__name__:
        status_code = status.HTTP_404_NOT_FOUND

    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "error": {
                "code": exc.__class__.__name__,
                "message": exc.message,
                "details": exc.details,
            },
        },
    )


@app.exception_handler(InfrastructureException)
async def infrastructure_exception_handler(request: Request, exc: InfrastructureException):
    """Handle infrastructure layer exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "code": exc.__class__.__name__,
                "message": "An internal error occurred",
                "details": exc.details if settings.DEBUG else {},
            },
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error": {
                "code": "ValidationError",
                "message": "Request validation failed",
                "details": {"errors": exc.errors()},
            },
        },
    )


# Include routers
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(images.router, prefix=settings.API_V1_PREFIX)
app.include_router(generations.router, prefix=settings.API_V1_PREFIX)


# Root endpoints
@app.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy",
        app=settings.APP_NAME,
        environment=settings.APP_ENV,
    )


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to OutfitLens API",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs",
        "health": "/health",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print(f"Starting {settings.APP_NAME} in {settings.APP_ENV} mode...")
    print(f"API documentation available at: {settings.API_V1_PREFIX}/docs")


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    print(f"Shutting down {settings.APP_NAME}...")
