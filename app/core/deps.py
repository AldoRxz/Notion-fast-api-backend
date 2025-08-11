
from fastapi import Depends, Header, HTTPException
import uuid
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.security.auth import decode_access_token
from app.core.errors import AuthenticationError, PermissionDenied


async def get_uow():
    async with SqlAlchemyUoW() as uow:
        yield uow


async def get_current_user_id(authorization: str | None = Header(default=None)) -> uuid.UUID:
    if not authorization or not authorization.startswith("Bearer "):
        raise AuthenticationError("Not authenticated")
    token = authorization.split(" ", 1)[1]
    sub = decode_access_token(token)
    if not sub:
        raise AuthenticationError("Invalid token")
    return uuid.UUID(sub)


async def ensure_workspace_member(workspace_id: uuid.UUID, user_id: uuid.UUID = Depends(get_current_user_id), uow: SqlAlchemyUoW = Depends(get_uow)) -> uuid.UUID:
    memberships = await uow.workspace_members.list_for_user(user_id)
    if not any(m.workspace_id == workspace_id for m in memberships):
        raise PermissionDenied("User is not a member of this workspace")
    return user_id
