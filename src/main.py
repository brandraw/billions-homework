from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.config import settings
from src.courses.router import router as courses_router
from src.enrollments.router import router as enrollments_router
from src.lectures.router import router as lectures_router
from src.payments.router import router as payments_router
from src.progress.router import router as progress_router
from src.reviews.router import router as reviews_router
from src.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="LMS API",
        description="Learning Management System - Inflearn-like backend",
        version="1.0.0",
        docs_url=None if settings.ENV == "production" else "/docs",
        redoc_url=None if settings.ENV == "production" else "/redoc",
        lifespan=lifespan,
    )

    app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
    app.include_router(users_router, prefix="/api/v1/users", tags=["users"])
    app.include_router(courses_router, prefix="/api/v1/courses", tags=["courses"])
    app.include_router(lectures_router, prefix="/api/v1", tags=["lectures"])
    app.include_router(enrollments_router, prefix="/api/v1/enrollments", tags=["enrollments"])
    app.include_router(payments_router, prefix="/api/v1/payments", tags=["payments"])
    app.include_router(progress_router, prefix="/api/v1/progress", tags=["progress"])
    app.include_router(reviews_router, prefix="/api/v1", tags=["reviews"])

    return app


app = create_app()
