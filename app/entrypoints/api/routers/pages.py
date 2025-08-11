from fastapi import APIRouter, Depends, HTTPException
import uuid
from app.application.dto import PageCreateDTO, PageReadDTO
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import Page, PageContent, PageType
<<<<<<< HEAD
from app.core.deps import get_uow, get_current_user_id, ensure_workspace_member
from sqlalchemy import select
from app.core.errors import NotFoundError, PermissionDenied
=======
from app.infrastructure.security.auth import decode_access_token
from fastapi import Header
>>>>>>> 3ee2475d47d2e49cf5e903bc3bb216afb1e7ac28

router = APIRouter(prefix="/pages", tags=["pages"])


<<<<<<< HEAD
=======
async def get_uow():
	async with SqlAlchemyUoW() as uow:
		yield uow


async def get_current_user_id(authorization: str | None = Header(default=None)) -> uuid.UUID:
	if not authorization or not authorization.startswith("Bearer "):
		raise HTTPException(status_code=401, detail="Not authenticated")
	token = authorization.split(" ", 1)[1]
	sub = decode_access_token(token)
	if not sub:
		raise HTTPException(status_code=401, detail="Invalid token")
	return uuid.UUID(sub)


>>>>>>> 3ee2475d47d2e49cf5e903bc3bb216afb1e7ac28
@router.post("/", response_model=PageReadDTO)
async def create_page(dto: PageCreateDTO, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	page = Page(
		workspace_id=dto.workspace_id,
		parent_page_id=dto.parent_page_id,
		title=dto.title,
		type=PageType(dto.type),
		created_by=user_id,
		updated_by=user_id,
	)
	await uow.pages.add(page)
	if dto.content is not None:
		content = PageContent(page=page, content=dto.content, meta={}, updated_by=user_id)
		await uow.page_contents.upsert(content)
	await uow.commit()
	return page
<<<<<<< HEAD


@router.get("/workspace/{workspace_id}", response_model=list[PageReadDTO])
async def list_pages(workspace_id: uuid.UUID, user_id: uuid.UUID = Depends(ensure_workspace_member), uow: SqlAlchemyUoW = Depends(get_uow)):
	# simple list (no hierarchy shaping yet)
	res = await uow.session.execute(select(Page).where(Page.workspace_id == workspace_id, Page.is_archived == False))  # type: ignore
	return list(res.scalars().all())


@router.get("/{page_id}", response_model=PageReadDTO)
async def get_page(page_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	page = await uow.pages.get(page_id)
	if not page or page.is_archived:
		raise NotFoundError("Page not found")
	await ensure_workspace_member(page.workspace_id, user_id, uow)  # permission check
	return page


class PageUpdateDTO(PageCreateDTO):
	workspace_id: uuid.UUID  # ensure present


@router.put("/{page_id}", response_model=PageReadDTO)
async def update_page(page_id: uuid.UUID, dto: PageUpdateDTO, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	page = await uow.pages.get(page_id)
	if not page:
		raise NotFoundError("Page not found")
	if page.workspace_id != dto.workspace_id:
		raise PermissionDenied("Cannot move page across workspaces")
	await ensure_workspace_member(page.workspace_id, user_id, uow)
	page.title = dto.title
	page.parent_page_id = dto.parent_page_id
	page.updated_by = user_id
	if dto.content is not None:
		existing = await uow.page_contents.get_by_page(page.id)
		if existing:
			existing.content = dto.content
			existing.updated_by = user_id
		else:
			await uow.page_contents.upsert(PageContent(page=page, content=dto.content, meta={}, updated_by=user_id))
	await uow.commit()
	return page


@router.delete("/{page_id}")
async def archive_page(page_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	page = await uow.pages.get(page_id)
	if not page:
		raise NotFoundError("Page not found")
	await ensure_workspace_member(page.workspace_id, user_id, uow)
	page.is_archived = True
	page.updated_by = user_id
	await uow.commit()
	return {"status": "archived"}
=======
>>>>>>> 3ee2475d47d2e49cf5e903bc3bb216afb1e7ac28
