from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from .engine import async_engine

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    expire_on_commit=False,
    autoflush=False,
    class_=AsyncSession,
)
