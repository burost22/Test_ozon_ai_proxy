from fastapi import APIRouter


router = APIRouter(tags=["История запросов"])


@router.get("/history",)
async def get_history_conversation():
    return {"Respoonse": "Respoonse"}
