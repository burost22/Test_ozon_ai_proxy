import pytest

from core.constants import MOCK_ANSWER


@pytest.mark.anyio
async def test_ask_in_mock_mode_returns_stub(client):
    response = await client.post("/api/ask", json={"question": "Привет"})

    assert response.status_code == 200
    assert response.json()["answer"] == MOCK_ANSWER
