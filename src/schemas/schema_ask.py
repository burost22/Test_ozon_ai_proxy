from pydantic import BaseModel, Field

from core.constants import MAX_LENGTH_ANS, MIN_LENGTH_ANS


class QuestionRequest(BaseModel):
    """Схема запроса к ЛЛМ"""

    question: str = Field(
        ...,
        description="Вопрос,отправляемый к ЛЛМ",
        example="Как дела?",
        min_length=MIN_LENGTH_ANS,
        max_length=MAX_LENGTH_ANS,
    )
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Как дела?",
            }
        }

class QuestionResponse(BaseModel):
    """Схема ответа от ЛЛМ"""

    answer: str = Field(
        ...,
        description="Ответ,получаемый от ЛЛМ",
        example="Я в порядке. Спасибо,что спросил. У тебя как ?",
    )
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Я в порядке. Спасибо,что спросил. У тебя как ?",
            }
        }
