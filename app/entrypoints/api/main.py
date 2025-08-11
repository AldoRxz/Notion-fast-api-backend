from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.entrypoints.api.routers.users import router as users_router
from app.entrypoints.api.routers.workspaces import router as workspaces_router
from app.entrypoints.api.routers.pages import router as pages_router
from app.core.errors import ERROR_CLASSES

app = FastAPI(title="Notion-like Backend")

app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(pages_router)


@app.get("/")
def root():
    return {"message": "Welcome to Notion FastAPI Backend!"}


@app.middleware("http")
async def domain_error_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except ERROR_CLASSES as e:  # type: ignore
        return JSONResponse(e.to_dict(), status_code=e.status_code)
