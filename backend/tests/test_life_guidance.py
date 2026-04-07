import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_list_problems(client: AsyncClient):
    response = await client.get("/api/life-guidance/problems")
    assert response.status_code == 200
    problems = response.json()
    assert len(problems) == 8
    assert problems[0]["id"] == "stress"


async def test_recommendations_unknown_problem(client: AsyncClient):
    response = await client.get("/api/life-guidance/recommendations", params={"problem": "unknown"})
    assert response.status_code == 200
    data = response.json()
    assert "error" in data


async def test_recommendations_empty_index(client: AsyncClient):
    response = await client.get("/api/life-guidance/recommendations", params={"problem": "stress"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
