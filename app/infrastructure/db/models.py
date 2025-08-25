import uuid
from sqlalchemy import (
	String, Boolean, ForeignKey, Text, UniqueConstraint, JSON
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from enum import Enum as PyEnum

from app.infrastructure.db.base import Base, TimestampMixin


class RoleName(str, PyEnum):
	owner = "owner"
	admin = "admin"
	editor = "editor"
	commenter = "commenter"
	viewer = "viewer"


class PageType(str, PyEnum):
	page = "page"
	database = "database"


class User(Base, TimestampMixin):
	__tablename__ = "users"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	password_hash: Mapped[str] = mapped_column(String, nullable=False)
	full_name: Mapped[str] = mapped_column(String, nullable=False)
	is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

	memberships: Mapped[list["WorkspaceMember"]] = relationship(back_populates="user")


class Workspace(Base, TimestampMixin):
	__tablename__ = "workspaces"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	name: Mapped[str] = mapped_column(String, nullable=False)
	slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
	created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

	members: Mapped[list["WorkspaceMember"]] = relationship(back_populates="workspace")
	pages: Mapped[list["Page"]] = relationship(back_populates="workspace")


class WorkspaceMember(Base):
	__tablename__ = "workspace_members"
	__table_args__ = (UniqueConstraint("workspace_id", "user_id", name="uq_workspace_user"),)

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
	user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
	role: Mapped[str] = mapped_column(String, default=RoleName.editor.value, nullable=False)

	workspace: Mapped[Workspace] = relationship(back_populates="members")
	user: Mapped[User] = relationship(back_populates="memberships")


class Page(Base, TimestampMixin):
	__tablename__ = "pages"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	workspace_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id", ondelete="CASCADE"), nullable=False)
	parent_page_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="SET NULL"))
	title: Mapped[str] = mapped_column(String, nullable=False)
	type: Mapped[str] = mapped_column(String, default=PageType.page.value, nullable=False)
	icon: Mapped[str | None] = mapped_column(String)
	cover_url: Mapped[str | None] = mapped_column(String)
	is_archived: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
	created_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
	updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

	workspace: Mapped[Workspace] = relationship(back_populates="pages")
	# Forward reference strings accepted by SQLAlchemy typing; use proper union inside the string
	content: Mapped["PageContent | None"] = relationship(back_populates="page", uselist=False)
	parent: Mapped["Page | None"] = relationship(remote_side=[id])


class PageContent(Base):
	__tablename__ = "page_content"

	id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
	page_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("pages.id", ondelete="CASCADE"), unique=True, nullable=False)
	content: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
	meta: Mapped[dict] = mapped_column(JSON, nullable=False, default=dict)
	updated_by: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

	page: Mapped[Page] = relationship(back_populates="content")


__all__ = [
	"User",
	"Workspace",
	"WorkspaceMember",
	"Page",
	"PageContent",
	"RoleName",
	"PageType",
]
