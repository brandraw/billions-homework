import uuid

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.courses.models import Course, CourseStatus
from src.courses.schemas import CourseListResponse
from src.database import get_db
from src.schemas import PaginatedResponse
from src.users import service
from src.users.models import User
from src.users.schemas import UserResponse, UserUpdateRequest

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
async def update_me(
    data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.update(db, current_user, data)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    return await service.get_by_id(db, user_id)


@router.get("/{user_id}/courses", response_model=list[CourseListResponse])
async def get_instructor_courses(
    user_id: uuid.UUID, db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Course)
        .where(
            Course.instructor_id == user_id,
            Course.status == CourseStatus.published,
        )
        .options(selectinload(Course.instructor))
        .order_by(Course.created_at.desc())
    )
    return result.scalars().all()
