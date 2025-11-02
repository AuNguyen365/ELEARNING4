from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1 import routes_auth, routes_user, routes_public, routes_private, routes_blog


app = FastAPI(
	title=settings.PROJECT_NAME,
	openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
)


# Set up CORS
if settings.BACKEND_CORS_ORIGINS:
	app.add_middleware(
		CORSMiddleware,
		allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)


# Public routes (no auth required)
app.include_router(routes_public.router, prefix=settings.API_V1_PREFIX)

# Auth routes (login, token)
app.include_router(routes_auth.router, prefix=settings.API_V1_PREFIX)

# User routes (mixed; some endpoints may require auth)
app.include_router(routes_user.router, prefix=settings.API_V1_PREFIX)

# Private routes (all endpoints here expect an authenticated user)
app.include_router(routes_private.router, prefix=settings.API_V1_PREFIX)
# Blog routes (CRUD + upload + search)
app.include_router(routes_blog.router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
def on_startup():
	# Create DB tables in dev environment; for production use Alembic migrations
	try:
		from app.db.init_db import create_tables

		create_tables()
	except Exception:
		# swallow errors here; better to log in real app
		pass

