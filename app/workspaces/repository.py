import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import Workspace, WorkspaceMember


class WorkspaceRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, ws: Workspace) -> None:
        self.session.add(ws)

    async def get(self, ws_id: uuid.UUID) -> Workspace | None:
        res = await self.session.execute(select(Workspace).where(Workspace.id == ws_id))
        return res.scalar_one_or_none()


class WorkspaceMemberRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, member: WorkspaceMember) -> None:
        self.session.add(member)

    async def list_for_user(self, user_id: uuid.UUID) -> list[WorkspaceMember]:
        from app.infrastructure.db.models import WorkspaceMember as WM
        res = await self.session.execute(select(WM).where(WM.user_id == user_id))
        return list(res.scalars().all())
