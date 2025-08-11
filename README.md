# Notion-fast-api-backend

Backend FastAPI (arquitectura hexagonal) para una app tipo Notion con contenido Yoopta.

## Endpoints principales

Auth
- POST /users/register  {email, password, full_name}
- POST /users/login (form-data) -> {access_token}

Workspaces
- POST /workspaces/  (Bearer) {name, slug?}
- GET  /workspaces/mine (Bearer)

Páginas
- POST   /pages/ (Bearer) {workspace_id, parent_page_id?, title, type, content?}
- GET    /pages/workspace/{workspace_id} (Bearer)
- GET    /pages/workspace/{workspace_id}/tree (Bearer)  -> árbol jerárquico
- GET    /pages/{page_id} (Bearer)
- PUT    /pages/{page_id} (Bearer)  actualiza título, parent y contenido
- PATCH  /pages/{page_id}/content (Bearer) actualiza parcial contenido/título
- DELETE /pages/{page_id} (Bearer) archiva la página

Sistema
- GET /health -> {status: ok}
- GET / -> mensaje base

## Formato JSON de contenido (Yoopta)
Contrato mínimo (puedes adaptarlo conforme al editor):
```
{
	"type": "doc",
	"version": 1,
	"content": [
		{ "type": "paragraph", "content": [{"type": "text", "text": "Hello"}] }
	]
}
```

## Autorización
- Token Bearer obligatorio para todos los endpoints (excepto root y health).
- Membership en workspace validada por dependencia ensure_workspace_member.

## CORS
Configurado vía FRONTEND_ORIGINS en .env (coma separada).

## Variables (.env ejemplo)
```
DATABASE_URL=postgresql+psycopg://app:app@db:5432/notion_local
SECRET_KEY=dev-secret
FRONTEND_ORIGINS=http://localhost:5173,http://localhost:3000
```

## Tests
Ejecutar: `pytest -q`
