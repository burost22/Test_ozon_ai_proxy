from datetime import datetime as dt
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class HistoryItem(BaseModel):
    """Схема одного экземпляра истории запрос-ответ от ЛЛМ."""

    question: str = Field(
        ...,
        description="Вопрос,заданный пользователем.",
    )
    answer: str = Field(
        ...,
        description="Ответ,полученный от ЛЛМ.",
    )
    timestamp: dt = Field(
        ...,
        description="дата и время вопроса.",
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "question": "Как дела?",
                "answer": "Я в порядке. Спасибо,что спросил. У тебя как ?",
                "timestamp": "2024-01-15T10:30:00",
            }
        }
    )


class HistoryResponse(BaseModel):
    """Схема ответа на получение последних 10 запросов к ЛЛМ."""

    items: List[HistoryItem] = Field(
        ...,
        description="Список последних запросов и ответов к ЛЛМ.",
    )
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "items": [
                    {
                        "question": "Как дела?",
                        "answer": ("Я в порядке.Спасибо,"
                                    "что спросил.У тебя как?"),
                        "timestamp": "2024-01-15T10:30:00",
                    },
                    {
                        "question": "Какая сегодня погода?",
                        "answer": "Пасмурно и хмуро,но морозно.",
                        "timestamp": "2024-02-15T11:35:00",
                    },
                ]
            }
        }
    )
