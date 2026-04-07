import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_search_short_query(client: AsyncClient):
    response = await client.get("/api/search", params={"q": "ab"})
    assert response.status_code == 422


async def test_search_empty_results(client: AsyncClient):
    response = await client.get("/api/search", params={"q": "nonexistentterm"})
    assert response.status_code == 200
    assert response.json() == []
