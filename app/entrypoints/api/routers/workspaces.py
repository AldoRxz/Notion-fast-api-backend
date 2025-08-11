from fastapi import APIRouter, Depends, HTTPException
import uuid
from slugify import slugify
from app.application.dto import WorkspaceCreateDTO, WorkspaceReadDTO
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import Workspace, WorkspaceMember, RoleName
from app.core.deps import get_uow, get_current_user_id

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


@router.post("/", response_model=WorkspaceReadDTO)
async def create_workspace(dto: WorkspaceCreateDTO, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	ws = Workspace(name=dto.name, slug=dto.slug or slugify(dto.name), created_by=user_id)
	await uow.workspaces.add(ws)
	member = WorkspaceMember(workspace_id=ws.id, user_id=user_id, role=RoleName.owner)
	await uow.workspace_members.add(member)
	await uow.commit()
	return ws


@router.get("/mine", response_model=list[WorkspaceReadDTO])
async def list_my_workspaces(user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)):
	memberships = await uow.workspace_members.list_for_user(user_id)
	# collect workspace objects (already loaded maybe lazy; re-fetch individually)
	result: list[Workspace] = []
	for m in memberships:
		ws = await uow.workspaces.get(m.workspace_id)
		if ws:
			result.append(ws)
	return result
