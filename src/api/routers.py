from fastapi import APIRouter

from api.endpoints import ask_router, history_router, streaming_router

main_router = APIRouter(prefix="/api")

main_router.include_router(ask_router)
main_router.include_router(history_router)
main_router.include_router(streaming_router)
