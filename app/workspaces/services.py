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
