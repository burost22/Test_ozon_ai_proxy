import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения для подключения переменных окружения."""

    title: str = "Заголовок"
    description: str = "Описание"
    version: str = "1.0.0"
    openai_api_key: str | None = None
    mock_mode: bool = True
    database_url: str
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    class Config:
        """Настройки конфигурации Pydantic."""
        env_file = ".env"
        extra = "ignore"
        env_file_encoding = "utf-8"


settings = Settings()
