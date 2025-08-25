import asyncio
import os
import pytest
import pytest_asyncio
import httpx
from app.main import app as fastapi_app

# Ensure selector loop policy on Windows for psycopg async compatibility
if os.name == "nt" and hasattr(asyncio, "WindowsSelectorEventLoopPolicy"):
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    except Exception:
        pass


@pytest.fixture(scope="session")
def event_loop():  # legacy workaround for pytest-asyncio strict mode
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def client():
    # ensure migrations run on startup inside test process
    os.environ.setdefault("AUTO_MIGRATE", "true")
    transport = httpx.ASGITransport(app=fastapi_app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
