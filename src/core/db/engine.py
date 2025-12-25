from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from ..config import settings

async_engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=True,
    future=True,
)
