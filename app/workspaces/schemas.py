import uuid
from pydantic import BaseModel

class WorkspaceCreateIn(BaseModel):
    name: str
    slug: str | None = None

class WorkspaceRead(BaseModel):
    id: uuid.UUID
    name: str
    slug: str
    class Config:
        from_attributes = True
