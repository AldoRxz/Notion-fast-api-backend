import uuid
from fastapi import APIRouter, Depends
from app.core.deps import get_uow, get_current_user_id
from app.infrastructure.db.uow import SqlAlchemyUoW
from . import schemas, services

router = APIRouter(prefix="/pages", tags=["pages_v2"])

@router.post("/", response_model=schemas.PageRead)
async def create(dto: schemas.PageCreateIn, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.create_page(uow, user_id, dto)

@router.get("/workspace/{workspace_id}", response_model=list[schemas.PageRead])
async def list_pages(workspace_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.get_pages(uow, workspace_id, user_id)

@router.get("/{page_id}", response_model=schemas.PageRead)
async def get_page(page_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.get_page(uow, page_id, user_id)

@router.put("/{page_id}", response_model=schemas.PageRead)
async def update_page(page_id: uuid.UUID, dto: schemas.PageUpdateIn, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.update_page(uow, page_id, user_id, dto)

@router.patch("/{page_id}/content")
async def patch_content(page_id: uuid.UUID, dto: schemas.PageContentPatch, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    await services.patch_page_content(uow, page_id, user_id, dto)
    return {"status": "updated"}

@router.delete("/{page_id}")
async def archive(page_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    await services.archive_page(uow, page_id, user_id)
    return {"status": "archived"}
