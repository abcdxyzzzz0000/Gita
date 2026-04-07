import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_health_check(client: AsyncClient):
    response = await client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


async def test_get_chapters_empty(client: AsyncClient):
    response = await client.get("/api/chapters")
    assert response.status_code == 200
    assert response.json() == []


async def test_get_shlokas_invalid_chapter(client: AsyncClient):
    response = await client.get("/api/chapters/0/shlokas")
    assert response.status_code == 400


async def test_get_shlokas_chapter_not_found(client: AsyncClient):
    response = await client.get("/api/chapters/1/shlokas")
    assert response.status_code == 404
