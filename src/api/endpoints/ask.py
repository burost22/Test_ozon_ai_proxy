from fastapi import APIRouter, HTTPException, status



router = APIRouter(tags=["Отправка запроса к LLM"])


@router.post(
    "/ask",
    status_code=status.HTTP_200_OK,
    summary="Запрос информации от ЛЛМ",
    description="",
)
async def post_question_to_llm():
    """"""
    return {"Respoonse": "Respoonse"}
