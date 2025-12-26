import asyncio

import uvicorn
from fastapi import FastAPI

from api.routers import main_router
from core.config import settings
from core.error_handlers import app_exception_handler
from core.exceptions import AppException
from core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger("ozon_app")
ozon_app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
)
ozon_app.include_router(main_router)
ozon_app.add_exception_handler(AppException, app_exception_handler)


async def fastapi_main() -> None:
    """Запуск сервера с бэкендом."""
    # Настраиваем конфигуратор:
    config = uvicorn.Config(
        "main:ozon_app",
        reload=True,
        host=settings.app_host,
        port=settings.app_port,
    )
    # Запускаем FastAPI сервер:
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(fastapi_main())
