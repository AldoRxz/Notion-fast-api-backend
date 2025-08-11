import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db import models


class SQLUserRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_by_email(self, email: str):
		res = await self.session.execute(select(models.User).where(models.User.email == email))
		return res.scalar_one_or_none()

	async def add(self, user: models.User):
		self.session.add(user)


class SQLWorkspaceRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def add(self, ws: models.Workspace):
		self.session.add(ws)

	async def get(self, ws_id: uuid.UUID):
		res = await self.session.execute(select(models.Workspace).where(models.Workspace.id == ws_id))
		return res.scalar_one_or_none()


class SQLWorkspaceMemberRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def add(self, member: models.WorkspaceMember):
		self.session.add(member)

	async def list_for_user(self, user_id: uuid.UUID):
		res = await self.session.execute(select(models.WorkspaceMember).where(models.WorkspaceMember.user_id == user_id))
		return list(res.scalars().all())


class SQLPageRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def add(self, page: models.Page):
		self.session.add(page)

	async def get(self, page_id: uuid.UUID):
		res = await self.session.execute(select(models.Page).where(models.Page.id == page_id))
		return res.scalar_one_or_none()


class SQLPageContentRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def upsert(self, content: models.PageContent):
		self.session.add(content)

	async def get_by_page(self, page_id: uuid.UUID):
		res = await self.session.execute(select(models.PageContent).where(models.PageContent.page_id == page_id))
		return res.scalar_one_or_none()

