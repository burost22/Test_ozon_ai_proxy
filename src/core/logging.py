import logging
from logging.config import dictConfig

LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "default": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
}


def setup_logging() -> None:
    """Настройка логирования."""
    dictConfig(LOG_CONFIG)


logger = logging.getLogger("src")
