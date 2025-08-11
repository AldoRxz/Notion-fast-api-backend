from pydantic import BaseModel, EmailStr
import uuid
from typing import Any


class UserRegisterDTO(BaseModel):
	email: EmailStr
	password: str
	full_name: str


class UserReadDTO(BaseModel):
	id: uuid.UUID
	email: EmailStr
	full_name: str

	class Config:
		from_attributes = True


class WorkspaceCreateDTO(BaseModel):
	name: str
	slug: str


class WorkspaceReadDTO(BaseModel):
	id: uuid.UUID
	name: str
	slug: str

	class Config:
		from_attributes = True


class PageCreateDTO(BaseModel):
	workspace_id: uuid.UUID
	parent_page_id: uuid.UUID | None = None
	title: str
	type: str = "page"
	content: Any | None = None


class PageReadDTO(BaseModel):
	id: uuid.UUID
	title: str

	class Config:
		from_attributes = True
