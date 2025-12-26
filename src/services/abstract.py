from abc import ABC, abstractmethod
from typing import Callable, Generic, TypeVar

from openai import AsyncOpenAI

from core.exceptions import InvalidQuestionError

T = TypeVar("T")


class BaseLLMAction(ABC, Generic[T]):
    """Шаблон действий (обычные и потоковые) для ЛЛМ с целью сохранения DRY."""

    def __init__(self, is_mock: bool, get_client: Callable[[], AsyncOpenAI]) -> None:
        self._is_mock = is_mock
        self._get_client = get_client

    async def __call__(self, question: str) -> T:
        if not question or not question.strip():
            raise InvalidQuestionError("Вопрос не может быть пустым")
        return await (self._mock(question) if self._is_mock else self._real(question))

    @abstractmethod
    async def _mock(self, question: str) -> T:
        pass

    @abstractmethod
    async def _real(self, question: str) -> T:
        pass
