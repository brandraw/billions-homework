import math
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, require_instructor
from src.courses import service
from src.courses.dependencies import get_course_or_404, get_section_or_404
from src.courses.models import Course, CourseLevel, Section
from src.courses.schemas import (
    CourseCreateRequest,
    CourseDetailResponse,
    CourseListResponse,
    CourseUpdateRequest,
    SectionCreateRequest,
    SectionResponse,
    SectionUpdateRequest,
)
from src.database import get_db
from src.schemas import PaginatedResponse
from src.users.models import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[CourseListResponse])
async def list_courses(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    category: str | None = Query(None),
    level: CourseLevel | None = Query(None),
    search: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    courses, total = await service.list_courses(
        db, page=page, size=size, category=category, level=level, search=search
    )
    return PaginatedResponse(
        items=courses,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


@router.post("", response_model=CourseDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_course(
    data: CourseCreateRequest,
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    return await service.create_course(db, current_user.id, data)


@router.get("/{course_id}", response_model=CourseDetailResponse)
async def get_course(course: Course = Depends(get_course_or_404)):
    return course


@router.patch("/{course_id}", response_model=CourseDetailResponse)
async def update_course(
    data: CourseUpdateRequest,
    course: Course = Depends(get_course_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    return await service.update_course(db, course, data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course: Course = Depends(get_course_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    await service.delete_course(db, course)


@router.post("/{course_id}/publish", response_model=CourseDetailResponse)
async def publish_course(
    course: Course = Depends(get_course_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    return await service.publish_course(db, course)


@router.post(
    "/{course_id}/sections",
    response_model=SectionResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_section(
    data: SectionCreateRequest,
    course: Course = Depends(get_course_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    return await service.create_section(db, course.id, data)


@router.patch("/{course_id}/sections/{section_id}", response_model=SectionResponse)
async def update_section(
    data: SectionUpdateRequest,
    course: Course = Depends(get_course_or_404),
    section: Section = Depends(get_section_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    return await service.update_section(db, section, data)


@router.delete(
    "/{course_id}/sections/{section_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_section(
    course: Course = Depends(get_course_or_404),
    section: Section = Depends(get_section_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await service.get_course_for_instructor(db, course.id, current_user.id)
    await service.delete_section(db, section)
