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
    """Реализует обработку запросов ЛЛМ с одним ответом как в фиктивном, так и в реальном режимах."""

    async def _mock(self, question: str) -> str:
        delay = random.uniform(START_DELAY, STOP_DELAY)
        await asyncio.sleep(delay)
        logger.info(f"Mock-режим: Обработка запроса (имитация задержки {delay:.2f} с")
        return MOCK_ANSWER

    async def _real(self, question: str) -> str:
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
            raise LLMServiceUnavailableError(f"ЛЛМ сервис недоступен: {str(e)}") from e
        except RateLimitError as e:
            logger.error(f"Превышен лимит частоты запросов к серверу OpenAI API: {e}")
            raise LLMRateLimitError(f"Превышен лимит частоты запросов: {str(e)}") from e
        except InternalServerError as e:
            logger.error(f"ошибка сервера у OpenAI API: {e}")
            raise LLMBadGatewayError(f"ошибка сервера у OpenAI API: {str(e)}") from e
        except Exception as e:
            logger.error(f"Неизвестная ошибка при запросе к ЛЛМ: {e}")
            raise LLMBadGatewayError(
                f"Неизвестная ошибка при запросе к ЛЛМ: {str(e)}"
            ) from e
