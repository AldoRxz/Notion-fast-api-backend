import asyncio
import os
import pytest
from httpx import AsyncClient
from fastapi import FastAPI
from app.entrypoints.api.main import app as fastapi_app

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop

@pytest.fixture()
async def client():
    # assumes DB is up & migrated
    async with AsyncClient(app=fastapi_app, base_url="http://test") as c:
        yield c
