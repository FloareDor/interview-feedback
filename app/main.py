from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core import users, interviews, pages
from app.database import create_tables

def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    origins = ["*"]

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    @_app.on_event("startup")
    def on_startup():
        create_tables()

    # Include the route files
    _app.include_router(users.router, prefix="/api/v1", tags=["users"])
    _app.include_router(interviews.router, prefix="/api/v1", tags=["interviews"])
    _app.include_router(pages.router, prefix="/api/v1", tags=["pages"])

    return _app

app = get_application()