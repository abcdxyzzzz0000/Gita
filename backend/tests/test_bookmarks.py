import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _register_and_get_headers(client: AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "bookmarkuser@test.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_list_bookmarks_unauthenticated(client: AsyncClient):
    response = await client.get("/api/bookmarks")
    assert response.status_code == 401


async def test_list_bookmarks_empty(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.get("/api/bookmarks", headers=headers)
    assert response.status_code == 200
    assert response.json() == []


async def test_create_bookmark(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.post(
        "/api/bookmarks",
        json={"chapter": 2, "shloka_number": 47},
        headers=headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["chapter"] == 2
    assert data["shloka_number"] == 47


async def test_create_duplicate_bookmark(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    await client.post(
        "/api/bookmarks",
        json={"chapter": 2, "shloka_number": 47},
        headers=headers,
    )
    response = await client.post(
        "/api/bookmarks",
        json={"chapter": 2, "shloka_number": 47},
        headers=headers,
    )
    assert response.status_code == 409


async def test_delete_bookmark(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    create_resp = await client.post(
        "/api/bookmarks",
        json={"chapter": 1, "shloka_number": 1},
        headers=headers,
    )
    bookmark_id = create_resp.json()["id"]

    response = await client.delete(f"/api/bookmarks/{bookmark_id}", headers=headers)
    assert response.status_code == 204

    # Verify it's gone
    list_resp = await client.get("/api/bookmarks", headers=headers)
    assert len(list_resp.json()) == 0
