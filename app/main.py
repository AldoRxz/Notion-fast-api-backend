from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from app.core.errors import ERROR_CLASSES
from app.core.config import settings
from app.users.router import router as users_router
from app.workspaces.router import router as workspaces_router
from app.pages.router import router as pages_router

app = FastAPI(title="Notion-like Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(pages_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Notion FastAPI Backend!"}

@app.on_event("startup")
async def run_startup_migrations_if_enabled():
    import os
    if os.getenv("AUTO_MIGRATE", "false").lower() in {"1", "true", "yes"}:
        import anyio
        from alembic.config import Config
        from alembic import command
        cfg = Config("alembic.ini")
        cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        def _upgrade():
            command.upgrade(cfg, "head")
        await anyio.to_thread.run_sync(_upgrade)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.middleware("http")
async def domain_error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ERROR_CLASSES as e:  # type: ignore
        return JSONResponse(e.to_dict(), status_code=e.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Invalid request",
            "details": exc.errors(),
        },
    )
