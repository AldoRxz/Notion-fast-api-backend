from fastapi import APIRouter, Depends, HTTPException
import uuid
from slugify import slugify
from app.application.dto import WorkspaceCreateDTO, WorkspaceReadDTO
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import Workspace, WorkspaceMember, RoleName
from app.infrastructure.security.auth import decode_access_token
from fastapi import Header

router = APIRouter(prefix="/workspaces", tags=["workspaces"])


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
