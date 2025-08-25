import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastructure.db.models import Page, PageContent


class PageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, page: Page) -> None:
        self.session.add(page)

    async def get(self, page_id: uuid.UUID) -> Page | None:
        res = await self.session.execute(select(Page).where(Page.id == page_id))
        return res.scalar_one_or_none()


class PageContentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert(self, content: PageContent) -> None:
        self.session.add(content)

    async def get_by_page(self, page_id: uuid.UUID) -> PageContent | None:
        res = await self.session.execute(select(PageContent).where(PageContent.page_id == page_id))
        return res.scalar_one_or_none()
