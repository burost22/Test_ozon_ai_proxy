from fastapi import APIRouter,Depends,status

from schemas.schema_history import HistoryItem,HistoryResponse
from core.db.models import HistoryModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.db.dependencies import init_async_session
from core.constants import LIMIT_COUNT
router = APIRouter(tags=["История запросов"])


@router.get("/history", status_code=status.HTTP_200_OK,summary="Получение списка из 10 послдених запросов и отвтетов к ЛЛМ",description="Очень хорошее описание",response_model=HistoryResponse)
async def get_history_conversation(session:AsyncSession =Depends(init_async_session))->HistoryResponse:
    """
    Docstring для get_history_conversation
    """
    history_response = select(HistoryModel).order_by(HistoryModel.timestamp.desc()).limit(LIMIT_COUNT)
    res = await session.execute(history_response)
    records = res.scalars().all()

    items=[HistoryItem(question=record.question,
                       answer=record.answer,
                       timestamp=record.timestamp) for record in records]
    return HistoryResponse(items=items)
