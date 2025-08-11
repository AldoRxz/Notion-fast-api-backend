
from contextlib import asynccontextmanager
from fastapi import Depends
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.base import async_session_maker

@asynccontextmanager
async def uow_context():
    async with SqlAlchemyUoW(async_session_maker) as uow:
        yield uow

def get_uow(uow=Depends(uow_context)):
    return uow
