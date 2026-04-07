import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_daily_wisdom_no_data(client: AsyncClient):
    """When no shlokas exist, returns a message."""
    response = await client.get("/api/daily-wisdom")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data or "shloka" in data


async def test_get_daily_wisdom_history_empty(client: AsyncClient):
    response = await client.get("/api/daily-wisdom/history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
