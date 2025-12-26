import asyncio
import random
from typing import AsyncGenerator

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


class StreamAction(BaseLLMAction):
    """Реализует потоковую передачу ответов ЛЛМ как в фиктивном, так и в реальном режимах."""

    async def _mock(self, question: str) -> AsyncGenerator[str, None]:
        delay = random.uniform(START_DELAY, STOP_DELAY)
        await asyncio.sleep(delay)
        logger.info(f"Mock-режим: Стриминг запроса (имитация задержки {delay:.2f} с")
        for word in MOCK_ANSWER.split():
            yield word + " "
            await asyncio.sleep(random.uniform(START_DELAY, STOP_DELAY))

    async def _real(self, question: str) -> AsyncGenerator[str, None]:
        client = self._get_client()
        try:
            logger.info("Отправка запроса к ЛЛМ.")
            stream = await client.chat.completions.create(
                model=LLM_MODEL,
                messages=[{"role": ROLE, "content": question}],
                temperature=TEMPERATURE,
                stream=True,
            )
            async for chunk in stream:
                yield chunk.choices[0].delta.content or ""
            yield "\n"
        except (APIConnectionError, APITimeoutError) as e:
            logger.error(f"Ошибка соединения с сервисом OpenAI API: {e}")
            raise LLMServiceUnavailableError(f"ЛЛМ сервис недоступен: {str(e)}") from e
        except RateLimitError as e:
            logger.error(f"Превышен лимит частоты запросов к серверу OpenAI API: {e}")
            raise LLMRateLimitError(f"Превышен лимит запросов: {str(e)}") from e
        except InternalServerError as e:
            logger.error(f"Ошибка сервера у OpenAI API: {e}")
            raise LLMBadGatewayError(f"Ошибка сервера у OpenAI API: {str(e)}") from e
