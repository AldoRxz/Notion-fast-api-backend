from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from datetime import datetime

from app.core.config import settings


class Base(DeclarativeBase):
	id: Mapped[str]

	@declared_attr.directive
	def __tablename__(cls) -> str:  # type: ignore
		return cls.__name__.lower()


class TimestampMixin:
	created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(
		DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
	)


"""Create the async SQLAlchemy engine.

We keep the ``postgresql+psycopg`` driver which already supports async (psycopg3)
instead of rewriting the URL to ``asyncpg``. The previous replacement caused a
ModuleNotFoundError because ``asyncpg`` wasn't installed. If you prefer the
``asyncpg`` driver, add it to dependencies and revert, but psycopg3 is fine.
"""

DATABASE_URL = settings.DATABASE_URL  # e.g. postgresql+psycopg://user:pass@host:port/db
engine = create_async_engine(DATABASE_URL, echo=False, future=True)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

__all__ = ["Base", "engine", "async_session_maker", "TimestampMixin"]
