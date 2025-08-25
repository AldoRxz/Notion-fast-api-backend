import uuid
import pytest


async def register_and_login(client, email: str | None = None):
    """Register a new user (unique email each invocation) and return JWT token.

    Using a unique email avoids cross-test contamination when the database
    persists between tests (e.g. real Postgres instead of an isolated transaction).
    """
    if email is None:
        email = f"user_{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": email,
        "password": "Secret123!",
        "full_name": "Test User"
    }
    r = await client.post("/users/register", json=payload)
    # If the email somehow already exists, fall back to login (idempotent behavior)
    if r.status_code not in (200, 400):
        assert False, r.text
    if r.status_code == 400:
        # ensure the error corresponds to existing user; then continue
        assert "already registered" in r.text.lower()
    r2 = await client.post("/users/login", data={"username": payload["email"], "password": payload["password"]})
    assert r2.status_code == 200, r2.text
    token = r2.json()["access_token"]
    return token


@pytest.mark.asyncio
async def test_create_workspace_and_page(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    unique_slug = f"my-ws-{uuid.uuid4().hex[:6]}"
    r = await client.post("/workspaces/", json={"name": "My WS", "slug": unique_slug}, headers=headers)
    assert r.status_code == 200, r.text
    ws_id = r.json()["id"]
    r2 = await client.post("/pages/", json={
        "workspace_id": ws_id,
        "title": "Home",
        "content": {"type": "doc", "content": []}
    }, headers=headers)
    assert r2.status_code == 200, r2.text
    page_id = r2.json()["id"]
    # list pages
    r3 = await client.get(f"/pages/workspace/{ws_id}", headers=headers)
    assert r3.status_code == 200
    assert any(p["id"] == page_id for p in r3.json())

@pytest.mark.asyncio
async def test_workspace_without_slug(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    unique_name = f"Another WS {uuid.uuid4().hex[:6]}"
    r = await client.post("/workspaces/", json={"name": unique_name}, headers=headers)
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["slug"].startswith("another-ws")
