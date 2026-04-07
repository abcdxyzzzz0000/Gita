import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_google_oauth_not_configured(client: AsyncClient):
    """When Google OAuth credentials aren't set, the endpoint returns 501."""
    response = await client.get("/api/auth/google", follow_redirects=False)
    assert response.status_code == 501


async def test_google_callback_not_configured(client: AsyncClient):
    response = await client.get("/api/auth/google/callback", params={"code": "test-code"})
    assert response.status_code == 501
