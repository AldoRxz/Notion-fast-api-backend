from fastapi import APIRouter, Depends, HTTPException
import uuid
from app.application.dto import PageCreateDTO, PageReadDTO
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import Page, PageContent, PageType
from app.infrastructure.security.auth import decode_access_token
from fastapi import Header

router = APIRouter(prefix="/pages", tags=["pages"])


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
