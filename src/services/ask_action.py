import asyncio
import random

from openai import (
    APIConnectionError,
    APITimeoutError,
    InternalServerError,
    RateLimitError,
)

from core.constants import (
    LLM_MODEL,
    MOCK_ANSWER,
    ROLE,
    START_DELAY,
    STOP_DELAY,
    TEMPERATURE,
)
from core.exceptions import (
    LLMBadGatewayError,
    LLMRateLimitError,
    LLMServiceUnavailableError,
)
from core.logging import get_logger
from services.abstract import BaseLLMAction

logger = get_logger("ozon_app")


class AskAction(BaseLLMAction):
    """
    Реализует обработку запросов ЛЛМ с одним
    ответом как в фиктивном, так и в реальном режимах.
    """

    async def _mock(self, question: str) -> str:
        """
            Моковый режим. После переопределения из
            базового класса возвращает Mock-заглушку.
        """
        delay = random.uniform(START_DELAY, STOP_DELAY)
        await asyncio.sleep(delay)
        logger.info(f"Mock-режим: Обработка "
                    f"запроса (имитация задержки {delay:.2f} с")
        return MOCK_ANSWER

    async def _real(self, question: str) -> str:
        """
            Моковый режим. После переопределения
            из базового класса возвращает ответ.
        """
        client = self._get_client()
        try:
            logger.info("Отправка запроса к ЛЛМ.")
            response = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": ROLE, "content": question}],
                temperature=TEMPERATURE,
            )
            answer = response.choices[0].message.content
            if not answer:
                raise LLMBadGatewayError("Пустой ответ от ЛЛМ.")
            logger.info("Успешно получен ответ от ЛЛМ.")
            return answer
        except (APIConnectionError, APITimeoutError) as e:
            logger.error(f"Ошибка соединения с сервисом OpenAI API: {e}")
            raise LLMServiceUnavailableError(f"ЛЛМ сервис"
                                             f" недоступен: {str(e)}") from e
        except RateLimitError as e:
            logger.error(f"Превышен лимит частоты запросов"
                         f" к серверу OpenAI API: {e}")
            raise LLMRateLimitError(f"Превышен лимит"
                                    f" запросов: {str(e)}") from e
        except InternalServerError as e:
            logger.error(f"Ошибка сервера у OpenAI API: {e}")
            raise LLMBadGatewayError(f"Ошибка сервера у "
                                     f"OpenAI API: {str(e)}") from e
