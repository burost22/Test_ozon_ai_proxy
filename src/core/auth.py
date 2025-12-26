from fastapi import Header

from core.config import settings
from core.exceptions import UnauthorizedError


async def verify_auth_token(authorization: str |
                            None = Header(default=None)
                            ) -> None:
    """
    Простая аутентификация на основе токенов
    с использованием заголовка Authorization.
    Если в переменной окружения установлен
    параметр AUTH_TOKEN, заголовок должен совпадать (с учетом регистра).
    """
    expected = settings.auth_token
    if not expected:
        return

    # Должны закинуть туда исходный токен,либо Bearer <token>
    token = authorization or ""
    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "", 1)

    if token != expected:
        raise UnauthorizedError("Неправильный или "
                                "пропущенный токен авторизации")
