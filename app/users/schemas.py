import uuid
from pydantic import BaseModel, EmailStr

class UserRegisterIn(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    class Config:
        from_attributes = True
