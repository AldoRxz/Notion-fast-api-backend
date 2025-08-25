from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.core.deps import get_uow
from app.infrastructure.db.uow import SqlAlchemyUoW
from . import schemas, services

router = APIRouter(prefix="/users", tags=["users_v2"])

@router.post("/register", response_model=schemas.UserRead)
async def register(dto: schemas.UserRegisterIn, uow: SqlAlchemyUoW = Depends(get_uow)):
    return await services.register_user(uow, dto)

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), uow: SqlAlchemyUoW = Depends(get_uow)):
    token = await services.login_user(uow, form.username, form.password)
    return {"access_token": token, "token_type": "bearer"}
