import uuid
from typing import Any
from pydantic import BaseModel

class PageCreateIn(BaseModel):
    workspace_id: uuid.UUID
    parent_page_id: uuid.UUID | None = None
    title: str
    type: str = "page"
    content: Any | None = None

class PageRead(BaseModel):
    id: uuid.UUID
    title: str
    parent_page_id: uuid.UUID | None = None
    type: str = "page"
    class Config:
        from_attributes = True

class PageWithContent(PageRead):
    content: Any | None = None

class PageUpdateIn(PageCreateIn):
    workspace_id: uuid.UUID

class PageContentPatch(BaseModel):
    title: str | None = None
    content: Any | None = None
