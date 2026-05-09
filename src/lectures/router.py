import uuid

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user, require_instructor
from src.courses.dependencies import get_course_or_404, get_section_or_404
from src.courses.models import Course, Section
from src.courses.service import get_course_for_instructor
from src.enrollments.models import Enrollment
from src.lectures import service
from src.lectures.dependencies import get_lecture_or_404
from src.lectures.exceptions import LectureAccessDenied
from src.lectures.models import Lecture
from src.lectures.schemas import LectureCreateRequest, LectureResponse, LectureUpdateRequest
from src.database import get_db
from src.users.models import User

router = APIRouter()


@router.post(
    "/courses/{course_id}/sections/{section_id}/lectures",
    response_model=LectureResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_lecture(
    data: LectureCreateRequest,
    course: Course = Depends(get_course_or_404),
    section: Section = Depends(get_section_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await get_course_for_instructor(db, course.id, current_user.id)
    return await service.create_lecture(db, section.id, data)


@router.get("/lectures/{lecture_id}", response_model=LectureResponse)
async def get_lecture(
    lecture: Lecture = Depends(get_lecture_or_404),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if lecture.is_preview:
        return lecture

    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == current_user.id,
            Enrollment.course_id == lecture.section.course_id,
        )
    )
    if not result.scalar_one_or_none():
        raise LectureAccessDenied()

    return lecture


@router.patch("/lectures/{lecture_id}", response_model=LectureResponse)
async def update_lecture(
    data: LectureUpdateRequest,
    lecture: Lecture = Depends(get_lecture_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await get_course_for_instructor(db, lecture.section.course_id, current_user.id)
    return await service.update_lecture(db, lecture, data)


@router.delete("/lectures/{lecture_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_lecture(
    lecture: Lecture = Depends(get_lecture_or_404),
    current_user: User = Depends(require_instructor),
    db: AsyncSession = Depends(get_db),
):
    await get_course_for_instructor(db, lecture.section.course_id, current_user.id)
    await service.delete_lecture(db, lecture)
