from fastapi import status


class AppException(Exception):
    """
        Базовый класс для кастомных исключений.
    """

    status_code: int = status.HTTP_400_BAD_REQUEST
    detail: str = "Ошибка приложения"

    def __init__(self, detail: str | None = None) -> None:
        """
            Инициализирует исключение
            с необязательным подробным сообщением.
        """
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class LLMServiceUnavailableError(AppException):
    """
        Возникает, когда служба языковой
        модели недоступна (ошибки подключения/тайм-аута).
    """

    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    detail = "сервис (LLM провайдер) недоступен"


class LLMBadGatewayError(AppException):
    """
        Возникает, когда служба LLM возвращает ошибку сервера.
    """

    status_code = status.HTTP_502_BAD_GATEWAY
    detail = "Не удалось отправить запрос к серверу и получить ответ "


class LLMRateLimitError(AppException):
    """
        Возникает, когда превышен лимит
        частоты запросов к сервису языковой модели.
    """

    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    detail = "Слишком много запросов"


class InvalidQuestionError(AppException):
    """
        Вопрос не прошёл валидацию.
    """

    status_code = status.HTTP_400_BAD_REQUEST
    detail = "Вопрос не может быть пустым"


class UnauthorizedError(AppException):
    """
        Ошибочная или отсутствующая авторизация.
    """

    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Неавторизовано"
