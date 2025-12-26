from fastapi import Request
from fastapi.responses import JSONResponse

from .exceptions import AppException
from .logging import get_logger
logger=get_logger("ozon_app")


async def app_exception_handler(
    request: Request,
    exc: AppException,
) -> JSONResponse:
    """Преобразует исключение в JSON-ответ и записывает его в лог."""
    logger.error("%s: %s", exc.__class__.__name__, exc.detail)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )
