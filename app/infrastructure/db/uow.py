from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.base import async_session_maker
from app.users.repository import UserRepository
from app.workspaces.repository import WorkspaceRepository, WorkspaceMemberRepository
from app.pages.repository import PageRepository, PageContentRepository


class SqlAlchemyUoW:
	def __init__(self, session_factory=async_session_maker):
		self._session_factory = session_factory
		self.session: AsyncSession | None = None
		# repositories
		self.users: UserRepository
		self.workspaces: WorkspaceRepository
		self.workspace_members: WorkspaceMemberRepository
		self.pages: PageRepository
		self.page_contents: PageContentRepository

	async def __aenter__(self):
		self.session = self._session_factory()
		self.users = UserRepository(self.session)
		self.workspaces = WorkspaceRepository(self.session)
		self.workspace_members = WorkspaceMemberRepository(self.session)
		self.pages = PageRepository(self.session)
		self.page_contents = PageContentRepository(self.session)
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
