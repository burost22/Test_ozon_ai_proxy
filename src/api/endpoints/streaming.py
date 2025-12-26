from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse

from schemas.schema_ask import QuestionRequest
from services.llm_client import llm_client

router = APIRouter(tags=["Отправка запроса к LLM c выводом текста постепенно"])


@router.post(
    "/streaming",
    status_code=status.HTTP_200_OK,
    summary="Запрос информации от ЛЛМ в режиме стриминга",
    description="Отправляет запрос к ЛЛМ, возвращает ответ в режиме стриминга",
    response_class=StreamingResponse,
    response_model=None,
)
async def post_question_to_llm_in_straming_mode(request: QuestionRequest):
    """
    Возвращает ответ в режима стриминга. Используется StreamingResponse FastApi

    Аргументы:
        request: Запрос с вопросом для ЛЛМ.

    Возвращает:
        ответ в режиме стриминга.
    """

    # Создаем генератор ,который будет получать поэтапно ответ от ЛЛМ
    async def generator():
        async for chunk in llm_client.stream_question(request.question):
            yield chunk

    return StreamingResponse(generator(), media_type="text/plain")
