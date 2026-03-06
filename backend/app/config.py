from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings from environment variables"""

    # API Keys
    google_api_key: str
    admin_key: str

    # Database
    database_url: str

    # CORS
    frontend_url: str = "http://localhost:5173"

    # App Config
    environment: str = "development"
    log_level: str = "info"
    max_conversation_length: int = 50

    # Rate Limiting
    rate_limit_per_minute: int = 20
    rate_limit_per_hour: int = 200

    # ChromaDB
    chroma_persist_directory: str = "data/chroma"
    chroma_collection_name: str = "paolo_knowledge"

    # Privacy
    conversation_retention_days: int = 365
    enable_conversation_storage: bool = True

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )

settings = Settings()
