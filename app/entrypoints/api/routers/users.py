from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import uuid
from app.application.dto import UserRegisterDTO, UserReadDTO
from app.infrastructure.db.uow import SqlAlchemyUoW
from app.infrastructure.db.models import User
from app.infrastructure.security.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/users", tags=["users"])


async def get_uow():
	async with SqlAlchemyUoW() as uow:
		yield uow


@router.post("/register", response_model=UserReadDTO)
async def register(dto: UserRegisterDTO, uow: SqlAlchemyUoW = Depends(get_uow)):
	existing = await uow.users.get_by_email(dto.email)
	if existing:
		raise HTTPException(status_code=400, detail="Email already registered")
	user = User(email=dto.email, password_hash=hash_password(dto.password), full_name=dto.full_name)
	await uow.users.add(user)
	await uow.commit()
	return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends(), uow: SqlAlchemyUoW = Depends(get_uow)):
	user = await uow.users.get_by_email(form.username)
	if not user or not verify_password(form.password, user.password_hash):
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
	token = create_access_token(str(user.id))
	return {"access_token": token, "token_type": "bearer"}
