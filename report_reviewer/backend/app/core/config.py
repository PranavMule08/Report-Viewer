from pydantic_settings import BaseSettings
from typing import Optional, List
from typing_extensions import Literal


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "AI-Powered Project Report Reviewer"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./reports.db"

    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production-abc123xyz"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days

    # OpenAI API
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.3
    OPENAI_BASE_URL: Optional[str] = None  # For custom API endpoints

    # File Upload
    MAX_FILE_SIZE_MB: int = 10
    MAX_FILE_SIZE_BYTES: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_EXTENSIONS: List[str] = []

    # AI Processing
    DEMO_MODE: bool = False  # Set to True for demo without API key
    CHUNK_SIZE: int = 2000  # Characters per chunk for large documents
    MAX_CHUNKS: int = 10  # Maximum chunks to process

    # CORS
    CORS_ORIGINS: List[str] = []

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()

# Set defaults if not configured
if not settings.ALLOWED_EXTENSIONS:
    settings.ALLOWED_EXTENSIONS = ["pdf", "docx", "txt"]

if not settings.CORS_ORIGINS:
    settings.CORS_ORIGINS = ["http://localhost:5173", "http://localhost:3000"]
