
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://app:app@localhost:5432/notion_local"
    SECRET_KEY: str = "dev-secret"
    FRONTEND_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 8
    ENV: str = "dev"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def origins_list(self) -> List[str]:
        return [o.strip() for o in self.FRONTEND_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()  # type: ignore


settings = get_settings()
