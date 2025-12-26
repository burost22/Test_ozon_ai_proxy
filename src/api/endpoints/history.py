from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.constants import LIMIT_COUNT
from core.db.dependencies import init_async_session
from core.db.models import HistoryModel
from schemas.schema_history import HistoryItem, HistoryResponse

router = APIRouter(tags=["История запросов"])


@router.get(
    "/history",
    status_code=status.HTTP_200_OK,
    summary="Получение списка из 10 послдених запросов и отвтетов к ЛЛМ",
    description="Очень хорошее описание",
    response_model=HistoryResponse,
)
async def get_history_conversation(
    session: AsyncSession = Depends(init_async_session),
) -> HistoryResponse:
    """
    Отправляет список из 10 последних
    айтемов (вопрос ответ со временем).

    Аргументы:
        session: Сессия базы данных для получения истории.

    Возвращает:
        список из 10 последних айтемов.
    """
    # берем нужные нам объекты модели,сортируя их,как нам нужно
    history_response = (
        select(HistoryModel
               ).order_by(HistoryModel.timestamp.desc()
                          ).limit(LIMIT_COUNT)
    )
    res = await session.execute(history_response)
    # распаковыаем кортежи и берем первое значение оттуда
    records = res.scalars().all()
    # Присваиваем каждому айтему ,на основании объекта модели,
    # нужные значения с помощь. list comprehension
    items = [
        HistoryItem(
            question=record.question,
            answer=record.answer,
            timestamp=record.timestamp
        )
        for record in records
    ]
    return HistoryResponse(items=items)
