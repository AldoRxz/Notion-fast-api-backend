
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+psycopg://app:app@localhost:5432/notion_local"
    SECRET_KEY: str = "dev-secret"

settings = Settings()
