import asyncio
import random
from typing import Optional

from openai import (
    APIConnectionError,
    APIError,
    APITimeoutError,
    AsyncOpenAI,
    InternalServerError,
    RateLimitError,
)

from core.config import settings
from core.constants import (
    BASE_URL_OPENROUTER,
    LLM_MODEL,
    MOCK_ANSWER,
    ROLE,
    START_DELAY,
    STOP_DELAY,
    TEMPERATURE,
)
from core.exceptions import (
    InvalidQuestionError,
    LLMBadGatewayError,
    LLMRateLimitError,
    LLMServiceUnavailableError,
)
from core.logging import get_logger

logger = get_logger("ozon_app")


class LLMClient:
    """Клиент для взаимодействия с языковой моделью (OpenAI или в режиме имитации)."""

    def __init__(self) -> None:
        """Инициализация ЛЛМ клиента."""
        self._client: Optional[AsyncOpenAI] = None
        self._is_mock_mode = self._check_mock_mode()

    @classmethod
    def _check_mock_mode(cls) -> bool:
        """
        Проверяет активацию Mock-режима.

        Mock_режим активируеция, если:
            MOCK_MODE =True , дефолтом False
            Нет API ключа для подключения к ЛЛМ
        """
        # Проверка флага MOCK_MODE
        mock_mode_env = getattr(settings, "mock_mode", None)
        if mock_mode_env is True or (
            isinstance(mock_mode_env, str) and mock_mode_env.lower() == "true"
        ):
            return True

        # Проверка наличия API ключа для доступа к ЛЛМ
        if not settings.openrouter_api_key or not settings.openrouter_api_key.strip():
            return True

        return False

    def _get_client(self) -> AsyncOpenAI:
        """Создание или получение асинхронного клиента для ЛЛМ"""
        if self._client is None:
            if settings.openrouter_api_key:
                self._client = AsyncOpenAI(
                    base_url=BASE_URL_OPENROUTER, api_key=settings.openrouter_api_key
                )
            else:
                raise ValueError("API ключ обязателен для реального режима работы.")

        return self._client

    async def _mock_ask(self, question: str) -> str:
        """
        Симуляция работы при Mock-режиме.

        Аргументы:
            question: вопрос к ЛЛМ

        Возврат:
            Mock-заглушка
        """
        delay = random.uniform(START_DELAY, STOP_DELAY)
        await asyncio.sleep(delay)

        logger.info(f"Mock-режим: Обработка запроса (имитация задержки {delay:.2f} с")
        return MOCK_ANSWER

    async def _real_ask(self, question: str) -> str:
        """
        Выполняет реальный запрос к API OpenAI.

        Аргументы:
            question: Вопрос, который нужно отправить языковой модели.

        Возврат:
            Ответ от языковой модели.

        Исключения:
            LLMServiceUnavailableError: Если произошла ошибка подключения/таймаута.
            LLMRateLimitError: Если превышен лимит запросов.
            LLMBadGatewayError: Если сервер возвращает ошибку 5xx.
            APIError: Для других ошибок API.
        """
        client = self._get_client()

        try:
            logger.info("Отправка запроса к ЛЛМ.")
            respoonse = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": ROLE, "content": question}],
                temperature=TEMPERATURE,
            )
            # Извлекаем нужный нам ответ
            answer = respoonse.choices[0].message.content
            if not answer:
                raise LLMBadGatewayError("Пустой ответ от ЛЛМ.")
            logger.info("Успешно получен ответ от ЛЛМ.")
            return answer

        except (APIConnectionError, APITimeoutError) as e:
            logger.error(f"Ошибка соединения с сервисом OpenAI API: {e}")
            raise LLMServiceUnavailableError(f"ЛЛМ сервис недоступен: {str(e)}") from e

        except RateLimitError as e:
            logger.error(f"Превышен лимит частоты запросов к серверу OpenAI API: {e}")
            raise LLMRateLimitError(f"Превышен лимит частоты запросов: {str(e)}") from e

        except InternalServerError as e:
            logger.error(f"ошибка сервера у OpenAI API: {e}")
            raise LLMBadGatewayError(f"ошибка сервера у OpenAI API: {str(e)}") from e

    async def ask_question(self, question: str) -> str:
        """
        LLMClient Задает вопрос к сервису
        При Mock-режиме возвращается заготовленный ответ
        При реальном запросе возвращается ответ от ЛЛМ.
        Аргументы:
            question: Вопрос, который нужно задать.

        Возвращает:
            Ответ от языковой модели
        """
        if not question or not question.strip():
            raise InvalidQuestionError("Вопрос не может быть пустым")

        if self._is_mock_mode:
            return await self._mock_ask(question)
        else:
            return await self._real_ask(question)


llm_client = LLMClient()
