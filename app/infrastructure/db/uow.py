from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.base import async_session_maker
from app.infrastructure.db.repositories import (
	SQLUserRepository,
	SQLWorkspaceRepository,
	SQLWorkspaceMemberRepository,
	SQLPageRepository,
	SQLPageContentRepository,
)


class SqlAlchemyUoW:
	def __init__(self, session_factory=async_session_maker):
		self._session_factory = session_factory
		self.session: AsyncSession | None = None
		# repositories
		self.users: SQLUserRepository
		self.workspaces: SQLWorkspaceRepository
		self.workspace_members: SQLWorkspaceMemberRepository
		self.pages: SQLPageRepository
		self.page_contents: SQLPageContentRepository

	async def __aenter__(self):
		self.session = self._session_factory()
		self.users = SQLUserRepository(self.session)
		self.workspaces = SQLWorkspaceRepository(self.session)
		self.workspace_members = SQLWorkspaceMemberRepository(self.session)
		self.pages = SQLPageRepository(self.session)
		self.page_contents = SQLPageContentRepository(self.session)
		return self

	async def __aexit__(self, exc_type, exc, tb):
		if exc:
			await self.session.rollback()  # type: ignore
		else:
			await self.session.commit()  # type: ignore
		await self.session.close()  # type: ignore

	async def commit(self):
		await self.session.commit()  # type: ignore

	async def rollback(self):
		await self.session.rollback()  # type: ignore


@asynccontextmanager
async def uow_context():
	async with SqlAlchemyUoW() as uow:
		yield uow
