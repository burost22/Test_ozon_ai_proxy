from fastapi import APIRouter

router = APIRouter(tags=["Отправка запроса к LLM c выводом текста постепенно"])


@router.post("/streaming")
async def post_question_to_llm_in_straming_mode():
    return {"Respoonse": "Respoonse"}
