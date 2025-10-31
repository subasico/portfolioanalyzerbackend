from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Portfolio Analyzer Backend"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # API Settings
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: str = "http://localhost:5000,https://allaboutai.com,https://www.allaboutai.com"

    # Database Settings
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/portfoliodb"

    # LLM Settings
    ANTHROPIC_API_KEY: str = ""
    OPENAI_API_KEY: str = ""
    LLM_PROVIDER: str = "anthropic"
    LLM_MODEL: str = "claude-3-5-sonnet-20241022"

    # Stock Data API
    ALPHA_VANTAGE_API_KEY: str = ""

    @property
    def cors_origins(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
