import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _register_and_get_headers(client: AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "accountuser@test.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_change_password(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.put(
        "/api/account/password",
        json={"current_password": "password123", "new_password": "newpassword123"},
        headers=headers,
    )
    assert response.status_code == 200

    # Login with new password
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": "accountuser@test.com", "password": "newpassword123"},
    )
    assert login_resp.status_code == 200


async def test_change_password_wrong_current(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.put(
        "/api/account/password",
        json={"current_password": "wrongpassword", "new_password": "newpassword123"},
        headers=headers,
    )
    assert response.status_code == 400


async def test_delete_account(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.delete("/api/account", headers=headers)
    assert response.status_code == 204

    # Login should fail
    login_resp = await client.post(
        "/api/auth/login",
        json={"email": "accountuser@test.com", "password": "password123"},
    )
    assert login_resp.status_code == 401
