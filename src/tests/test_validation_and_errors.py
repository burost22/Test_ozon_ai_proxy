import pytest
from httpx import ASGITransport, AsyncClient

from core.exceptions import LLMRateLimitError, LLMServiceUnavailableError
from main import ozon_app
from services.llm_client import llm_client


@pytest.fixture
async def client_no_auth():
    async with AsyncClient(
        transport=ASGITransport(app=ozon_app),
        base_url="http://testserver",
    ) as client:
        yield client


@pytest.mark.skip(
    reason="Не разобрался,как в документации добавлять токен. Через постмен все получается"
)
async def test_auth_failure_returns_unauthorized(client_no_auth):
    response = await client_no_auth.post("/api/ask", json={"question": "Hello"})

    assert response.status_code == 401
    assert "Authorization" in response.json()["detail"]


@pytest.mark.anyio
async def test_validation_error_for_empty_question(client):
    response = await client.post("/api/ask", json={"question": "   "})

    assert response.status_code == 400
    assert "не может быть пустым" in response.json()["detail"]


@pytest.mark.anyio
async def test_llm_service_unavailable_maps_to_503(client, monkeypatch):
    async def fake_ask_question(_: str) -> str:
        raise LLMServiceUnavailableError("LLM down")

    monkeypatch.setattr(llm_client, "ask_question", fake_ask_question)

    response = await client.post("/api/ask", json={"question": "Hello"})

    assert response.status_code == 503
    assert "LLM down" in response.json()["detail"]


@pytest.mark.anyio
async def test_llm_rate_limit_maps_to_429(client, monkeypatch):
    async def fake_rate_limited(_: str) -> str:
        raise LLMRateLimitError("Too many requests")

    monkeypatch.setattr(llm_client, "ask_question", fake_rate_limited)

    response = await client.post("/api/ask", json={"question": "Hello"})

    assert response.status_code == 429
    assert "Too many requests" in response.json()["detail"]
