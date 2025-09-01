import uuid
from slugify import slugify
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.infrastructure.db.models import Workspace, WorkspaceMember, RoleName
from app.infrastructure.db.uow import SqlAlchemyUoW
from . import schemas

async def create_workspace(uow: SqlAlchemyUoW, user_id: uuid.UUID, data: schemas.WorkspaceCreateIn) -> Workspace:
    slug = data.slug or slugify(data.name)
    ws = Workspace(id=uuid.uuid4(), name=data.name, slug=slug, created_by=user_id)
    await uow.workspaces.add(ws)
    member = WorkspaceMember(workspace_id=ws.id, user_id=user_id, role=RoleName.owner)
    await uow.workspace_members.add(member)
    try:
        await uow.commit()
    except IntegrityError as e:
        await uow.rollback()
        raise HTTPException(status_code=400, detail="Slug already exists") from e
    return ws

async def list_workspaces(uow: SqlAlchemyUoW, user_id: uuid.UUID) -> list[Workspace]:
    memberships = await uow.workspace_members.list_for_user(user_id)
    workspaces: list[Workspace] = []
    for m in memberships:
        ws = await uow.workspaces.get(m.workspace_id)
        if ws:
            workspaces.append(ws)
    return workspaces

async def delete_workspace(uow: SqlAlchemyUoW, user_id: uuid.UUID, workspace_id: uuid.UUID) -> None:
    ws = await uow.workspaces.get(workspace_id)
    if not ws:
        return
    # Only owner can delete for now
    membership = await uow.workspace_members.get_by_workspace_user(workspace_id, user_id)
    if not membership or membership.role != RoleName.owner:
        raise HTTPException(status_code=403, detail="Not allowed")
    await uow.session.delete(ws)
    await uow.commit()
