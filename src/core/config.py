from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения для подключения переменных окружения."""

    title: str = "Заголовок"
    description: str = "Описание"
    version: str = "1.0.0"
    openrouter_api_key: str | None = None
    mock_mode: bool = False
    database_url: str = "sqlite+aiosqlite:///./history.db"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"

    model_config = ConfigDict(
        env_file=".env",
        extra="ignore",
        env_file_encoding="utf-8",
    )


settings = Settings()
