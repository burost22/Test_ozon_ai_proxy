import os
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

# Проверка пути. Нужно,чтобы избежать ошибки с путем
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

# Дефолтные переменные для тестов
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("AUTH_TOKEN", "test-token")
os.environ.setdefault("MOCK_MODE", "true")

from core.db.dependencies import init_async_session
from core.db.models import Base
from main import ozon_app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


# Создаем движок
@pytest.fixture(scope="session")
async def async_engine():
    engine = create_async_engine(
        os.getenv("DATABASE_URL"),
        echo=False,
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()


# Создаем сессию
@pytest.fixture(scope="session")
def session_maker(async_engine):
    return async_sessionmaker(
        async_engine,
        expire_on_commit=False,
        autoflush=False,
        class_=AsyncSession,
    )


@pytest.fixture(autouse=True, scope="session")
def override_db_dependency(session_maker):
    async def _get_session() -> AsyncGenerator[AsyncSession, None]:
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    ozon_app.dependency_overrides[init_async_session] = _get_session
    yield
    ozon_app.dependency_overrides.clear()


@pytest.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=ozon_app),
        base_url="http://testserver",
        headers={"Authorization": "Bearer test-token"},
    ) as client:
        yield client
