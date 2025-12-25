from fastapi import APIRouter

from schemas.schema_history import HistoryResponse

router = APIRouter(tags=["История запросов"])


@router.get("/history", response_model=HistoryResponse)
async def get_history_conversation():
    return {"Respoonse": "Respoonse"}
