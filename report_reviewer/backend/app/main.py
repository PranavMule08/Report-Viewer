import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.db.session import init_db, close_db
from app.api.deps import api_router
from app.services.ai_service import AIService
from app.services.demo_service import DemoService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    logger.info("Starting AI-Powered Project Report Reviewer...")
    logger.info(f"Demo mode: {settings.DEMO_MODE}")
    logger.info(f"OpenAI API configured: {bool(settings.OPENAI_API_KEY)}")

    # Initialize database
    await init_db()
    logger.info("Database initialized")

    # Create uploads directory
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    yield

    # Shutdown
    logger.info("Shutting down...")
    await close_db()


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-Powered Project Report Reviewer and Improvement Assistant",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_PREFIX)

# Serve uploaded files (for download)
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.get("/")
async def root():
    """Root endpoint - API info."""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "demo_mode": settings.DEMO_MODE,
        "api_endpoint": f"{settings.API_V1_PREFIX}"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/v1/config", tags=["Configuration"])
async def get_config():
    """Get application configuration (excluding sensitive data)."""
    return {
        "demo_mode": settings.DEMO_MODE,
        "max_file_size_mb": settings.MAX_FILE_SIZE_MB,
        "allowed_extensions": settings.ALLOWED_EXTENSIONS,
        "openai_configured": bool(settings.OPENAI_API_KEY),
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
