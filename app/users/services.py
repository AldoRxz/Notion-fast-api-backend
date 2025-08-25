import uuid
from app.infrastructure.db.models import User
from app.infrastructure.security.auth import hash_password, verify_password, create_access_token
from . import schemas
from app.infrastructure.db.uow import SqlAlchemyUoW
from fastapi import HTTPException, status

async def register_user(uow: SqlAlchemyUoW, data: schemas.UserRegisterIn) -> User:
    existing = await uow.users.get_by_email(data.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, password_hash=hash_password(data.password), full_name=data.full_name)
    await uow.users.add(user)
    await uow.commit()
    return user

async def login_user(uow: SqlAlchemyUoW, username: str, password: str) -> str:
    user = await uow.users.get_by_email(username)
    if not user or not verify_password(password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return create_access_token(str(user.id))
