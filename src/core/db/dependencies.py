from typing import AsyncGenerator
from .session import AsyncSessionLocal



async def init_async_session() -> AsyncGenerator:
    """
    Dependency для получения сессии базы данных.

    Yields:
        AsyncSession: Сессия базы данных
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

