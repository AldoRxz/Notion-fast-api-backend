import uuid
from fastapi import APIRouter, Depends
from app.core.deps import get_uow, get_current_user_id
from app.infrastructure.db.uow import SqlAlchemyUoW
from . import schemas, services

router = APIRouter(prefix="/workspaces", tags=["workspaces_v2"])

@router.post("/", response_model=schemas.WorkspaceRead)
async def create(dto: schemas.WorkspaceCreateIn, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.create_workspace(uow, user_id, dto)

@router.get("/", response_model=list[schemas.WorkspaceRead])
async def list_my_workspaces(user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.list_workspaces(uow, user_id)
