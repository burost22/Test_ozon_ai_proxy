from fastapi import APIRouter, HTTPException, status

from schemas.schema_ask import QuestionRequest, QuestionResponse

router = APIRouter(tags=["Отправка запроса к LLM"])


@router.post(
    "/ask",
    response_model=QuestionResponse,
    status_code=status.HTTP_200_OK,
    summary="Запрос информации от ЛЛМ",
    description="",
)
async def post_question_to_llm(request: QuestionRequest) -> QuestionResponse:
    """"""
    return {"Respoonse": "Respoonse"}
