import uuid
from sqlalchemy import select
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import Page, PageContent, PageType
from app.core.errors import NotFoundError, PermissionDenied
from app.core.deps import ensure_workspace_member
from . import schemas

async def create_page(uow: SqlAlchemyUoW, user_id: uuid.UUID, data: schemas.PageCreateIn) -> Page:
    await ensure_workspace_member(data.workspace_id, user_id, uow)
    page = Page(
        workspace_id=data.workspace_id,
        parent_page_id=data.parent_page_id,
        title=data.title,
        type=PageType(data.type),
        created_by=user_id,
        updated_by=user_id,
    )
    await uow.pages.add(page)
    if data.content is not None:
        content = PageContent(page=page, content=data.content, meta={}, updated_by=user_id)
        await uow.page_contents.upsert(content)
    await uow.commit()
    return page

async def get_pages(uow: SqlAlchemyUoW, workspace_id: uuid.UUID, user_id: uuid.UUID) -> list[Page]:
    await ensure_workspace_member(workspace_id, user_id, uow)
    res = await uow.session.execute(select(Page).where(Page.workspace_id == workspace_id, Page.is_archived == False))  # type: ignore
    return list(res.scalars().all())

async def get_page(uow: SqlAlchemyUoW, page_id: uuid.UUID, user_id: uuid.UUID) -> Page:
    page = await uow.pages.get(page_id)
    if not page or page.is_archived:
        raise NotFoundError("Page not found")
    await ensure_workspace_member(page.workspace_id, user_id, uow)
    return page

async def update_page(uow: SqlAlchemyUoW, page_id: uuid.UUID, user_id: uuid.UUID, data: schemas.PageUpdateIn) -> Page:
    page = await uow.pages.get(page_id)
    if not page:
        raise NotFoundError("Page not found")
    if page.workspace_id != data.workspace_id:
        raise PermissionDenied("Cannot move page across workspaces")
    await ensure_workspace_member(page.workspace_id, user_id, uow)
    page.title = data.title
    page.parent_page_id = data.parent_page_id
    page.updated_by = user_id
    if data.content is not None:
        existing = await uow.page_contents.get_by_page(page.id)
        if existing:
            existing.content = data.content
            existing.updated_by = user_id
        else:
            await uow.page_contents.upsert(PageContent(page=page, content=data.content, meta={}, updated_by=user_id))
    await uow.commit()
    return page

async def patch_page_content(uow: SqlAlchemyUoW, page_id: uuid.UUID, user_id: uuid.UUID, data: schemas.PageContentPatch) -> None:
    page = await uow.pages.get(page_id)
    if not page:
        raise NotFoundError("Page not found")
    await ensure_workspace_member(page.workspace_id, user_id, uow)
    if data.title is not None:
        page.title = data.title
    if data.content is not None:
        existing = await uow.page_contents.get_by_page(page.id)
        if existing:
            existing.content = data.content
            existing.updated_by = user_id
        else:
            await uow.page_contents.upsert(PageContent(page=page, content=data.content, meta={}, updated_by=user_id))
    page.updated_by = user_id
    await uow.commit()

async def archive_page(uow: SqlAlchemyUoW, page_id: uuid.UUID, user_id: uuid.UUID) -> None:
    page = await uow.pages.get(page_id)
    if not page:
        raise NotFoundError("Page not found")
    await ensure_workspace_member(page.workspace_id, user_id, uow)
    page.is_archived = True
    page.updated_by = user_id
    await uow.commit()
