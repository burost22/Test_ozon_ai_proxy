import asyncio
import time

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

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


@ozon_app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log method, path, status, and duration for each request."""
    start = time.perf_counter()
    response: Response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "request method=%s path=%s status=%s duration_ms=%.2f",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


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
