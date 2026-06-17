"""
Configuration Management for Prescriptive Maintenance RAG Agent.
This module handles all environment variables and configuration settings.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

class Settings(BaseSettings):
    """
    Project settings loaded from environment variables and/or .env file.
    """
    # Project Settings
    PROJECT_NAME: str = "Prescriptive Maintenance RAG Agent"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # Paths
    LOGS_DIR: Path = BASE_DIR / "logs"
    CHROMA_DB_DIR: Path = BASE_DIR / "chroma_db"

    # LLM Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4-turbo")

    # RAG Settings
    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 100

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

# Global settings instance to be imported across the project
settings = Settings()

# Ensure necessary directories exist
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
settings.CHROMA_DB_DIR.mkdir(parents=True, exist_ok=True)
