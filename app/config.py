"""Application configuration loaded from environment variables."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings for the Expense Tracker API."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = "sqlite:///./expenses.db"
    APP_NAME: str = "Expense Tracker API"
    APP_VERSION: str = "1.0.0"


settings = Settings()