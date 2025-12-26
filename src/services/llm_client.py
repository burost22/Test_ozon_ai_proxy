from typing import AsyncGenerator, Optional

from openai import AsyncOpenAI

from core.config import settings
from core.constants import BASE_URL_OPENROUTER
from core.logging import get_logger
from services.ask_action import AskAction
from services.stream_action import StreamAction

logger = get_logger("ozon_app")


class LLMClient:
    """Клиент для взаимодействия с языковой моделью (OpenAI или в режиме имитации)."""

    def __init__(self) -> None:
        self._client: Optional[AsyncOpenAI] = None
        self._is_mock_mode = self._check_mock_mode()
        # Не забываем про DRY . Создаем действия,чтобы не повторяться)
        self._ask_action = AskAction(self._is_mock_mode, self._get_client)
        self._stream_action = StreamAction(self._is_mock_mode, self._get_client)

    @classmethod
    def _check_mock_mode(cls) -> bool:
        mock_mode_env = getattr(settings, "mock_mode", None)
        if mock_mode_env is True or (
            isinstance(mock_mode_env, str) and mock_mode_env.lower() == "true"
        ):
            return True
        return (
            not settings.openrouter_api_key or not settings.openrouter_api_key.strip()
        )

    def _get_client(self) -> AsyncOpenAI:
        if self._client is None:
            if settings.openrouter_api_key:
                self._client = AsyncOpenAI(
                    base_url=BASE_URL_OPENROUTER, api_key=settings.openrouter_api_key
                )
            else:
                raise ValueError("API ключ обязателен для реального режима работы.")
        return self._client

    async def ask_question(self, question: str) -> str:
        return await self._ask_action(question)

    async def stream_question(self, question: str) -> AsyncGenerator[str, None]:
        stream = await self._stream_action(question)
        async for chunk in stream:
            yield chunk


llm_client = LLMClient()
