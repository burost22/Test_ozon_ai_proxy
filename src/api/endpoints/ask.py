from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.db.dependencies import init_async_session
from core.db.models import HistoryModel
from schemas.schema_ask import QuestionRequest, QuestionResponse
from services.llm_client import llm_client

router = APIRouter(tags=["Отправка запроса к LLM"])


@router.post(
    "/ask",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Запрос информации от ЛЛМ",
    description="Отправляет запрос к ЛЛМ, возвращает ответ."
    "Вопрос-ответ сохраняется в БД для дальнейшего использования",
)
async def post_question_to_llm(
    request: QuestionRequest,
    session: AsyncSession = Depends(init_async_session)
) -> QuestionResponse:
    """
    Отправляет вопрос к языковой модели и возвращает ответ.

    Аргументы:
        request: Запрос с вопросом для ЛЛМ.
        session: Сессия базы данных для сохранения истории.

    Возвращает:
        Ответ от языковой модели.

    Исключения:
        LLMServiceUnavailableError: Если ЛЛМ сервис недоступен (503).
        LLMBadGatewayError: Если ЛЛМ сервис вернул ошибку сервера (502).
        LLMRateLimitError: Если превышен лимит запросов (429).
    """

    # получаем ответ от ЛЛМ
    answer = await llm_client.ask_question(request.question)

    # Записываем В БД ответ
    history_record = HistoryModel(
        question=request.question,
        answer=answer,
    )
    session.add(history_record)
    await session.flush()  # Получаем ID экземпляра записи

    return QuestionResponse(answer=answer)
