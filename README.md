# Notion-fast-api-backend

Backend FastAPI con estructura vertical slice (users, workspaces, pages) para una app tipo Notion (contenido Yoopta / JSON rich text).

## Estructura actual

```
app/
	core/            # config, deps, errors, auth helpers
	users/           # router, schemas, services, repository
	workspaces/      # router, schemas, services, repository
	pages/           # router, schemas, services, repository
	infrastructure/
		db/            # base SQLAlchemy, session, uow
		security/      # auth helpers (hash, jwt)
migrations/
tests/
```

## Endpoints principales (v2 routers)

Auth
- POST /users/register  {email, password, full_name}
- POST /users/login (form-data) -> {access_token}

Workspaces
- POST /workspaces/  (Bearer) {name, slug?}
	(Listado /mine aún por reintroducir si es necesario)

Páginas
- POST   /pages/ (Bearer) {workspace_id, parent_page_id?, title, type, content?}
- GET    /pages/workspace/{workspace_id} (Bearer)
- GET    /pages/{page_id} (Bearer)
- PUT    /pages/{page_id} (Bearer)
- PATCH  /pages/{page_id}/content (Bearer)
- DELETE /pages/{page_id} (Bearer)
	(Árbol /tree pendiente de migrar)

Sistema
- GET /health -> {status: ok}
- GET / -> mensaje base


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

Ejecutar:
```
pytest -q
```

Cobertura actual: auth flow, creación workspace (sin slug), creación/listado de páginas básicas.

## Próximos pasos sugeridos
- Reintroducir /workspaces/mine y /pages/.../tree si se requieren.
- Endpoint de detalle de página con contenido completo.
- Versionado de contenido (opcional).
- Más tests de permisos y edge cases.
