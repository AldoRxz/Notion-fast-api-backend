import uuid
import pytest


async def register_and_login(client):
    r = await client.post("/users/register", json={
        "email": "user@example.com",
        "password": "Secret123!",
        "full_name": "Test User"
    })
    assert r.status_code == 200, r.text
    r2 = await client.post("/users/login", data={"username": "user@example.com", "password": "Secret123!"})
    assert r2.status_code == 200, r2.text
    token = r2.json()["access_token"]
    return token


@pytest.mark.asyncio
async def test_create_workspace_and_page(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    r = await client.post("/workspaces/", json={"name": "My WS", "slug": "my-ws"}, headers=headers)
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
