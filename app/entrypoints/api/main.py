from fastapi import FastAPI
from app.entrypoints.api.routers.users import router as users_router
from app.entrypoints.api.routers.workspaces import router as workspaces_router
from app.entrypoints.api.routers.pages import router as pages_router

app = FastAPI(title="Notion-like Backend")

app.include_router(users_router)
app.include_router(workspaces_router)
app.include_router(pages_router)


@app.get("/")
def root():
    return {"message": "Welcome to Notion FastAPI Backend!"}
