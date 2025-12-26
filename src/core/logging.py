# import logging
# from logging.config import dictConfig

# LOG_CONFIG = {
#     "version": 1,
#     "formatters": {
#         "default": {
#             "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
#         },
#     },
#     "handlers": {
#         "console": {
#             "class": "logging.StreamHandler",
#             "formatter": "default",
#         },
#     },
#     "root": {
#         "level": "INFO",
#         "handlers": ["console"],
#     },
# }


# def setup_logging() -> None:
#     """Настройка логирования."""
#     dictConfig(LOG_CONFIG)


# logger = logging.getLogger("src")
# import logging


# async def configure_logger() -> None:
#     """Configure built-in logger."""
#     logging.basicConfig(
#         level=logging.INFO,
#         format="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
#     )


import logging
import os
import sys
from logging import Logger
from typing import Any, Dict


def configure_logging(level: str | None = None) -> None:
    """
    Конфигурирует глобальный логгер приложения.

    level: уровень логирования (например 'INFO'/'DEBUG'). Если None — берём из env LOG_LEVEL.
    """
    log_level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()

    # Настройка простого форматтера с временной меткой (ISO-like)
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s %(message)s", "%Y-%m-%dT%H:%M:%S"
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
