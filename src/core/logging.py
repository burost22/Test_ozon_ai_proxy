import logging
import os
import sys
from logging import Logger


def configure_logging(level: str | None = None) -> None:
    """
    Конфигурирует глобальный логгер приложения.

    level: уровень логирования (например 'INFO'/'DEBUG').
    Если None — берём из env LOG_LEVEL.
    """
    log_level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()

    # Настройка простого форматтера с временной меткой (ISO-like)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s",
        "%Y-%m-%dT%H:%M:%S"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root = logging.getLogger()
    # Удаляем старые handlers (например Uvicorn добавляет свои)
    if root.handlers:
        for h in list(root.handlers):
            root.removeHandler(h)

    root.setLevel(getattr(logging, log_level, logging.INFO))
    root.addHandler(handler)

    # Настройки для внешних библиотек — чтобы не засоряли лог
    logging.getLogger("uvicorn").handlers = [handler]
    logging.getLogger("uvicorn.error").handlers = [handler]
    logging.getLogger("uvicorn.access").handlers = [handler]


def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
