import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_db
from src.progress import service
from src.progress.schemas import (
    CourseProgressResponse,
    LectureProgressResponse,
    UpdateProgressRequest,
)
from src.users.models import User

router = APIRouter()


@router.get("/courses/{course_id}", response_model=CourseProgressResponse)
async def get_course_progress(
    course_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_course_progress(db, current_user.id, course_id)


@router.post("/lectures/{lecture_id}", response_model=LectureProgressResponse)
async def update_lecture_progress(
    lecture_id: uuid.UUID,
    data: UpdateProgressRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.upsert_progress(
        db,
        user_id=current_user.id,
        lecture_id=lecture_id,
        watched_seconds=data.watched_seconds,
        is_completed=data.is_completed,
    )
