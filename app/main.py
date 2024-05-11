from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core import users, interviews, pages

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include the route files
    _app.include_router(users.router, prefix="/api/v1", tags=["users"])
    # _app.include_router(interviews.router, prefix="/api/v1", tags=["interviews"])
    # _app.include_router(pages.router, prefix="/api/v1", tags=["pages"])

    return _app

app = get_application()