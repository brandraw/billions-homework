import uuid
from datetime import datetime, timezone

from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.enrollments.service import is_enrolled
from src.exceptions import PermissionDenied
from src.lectures.models import Lecture
from src.progress.models import LectureProgress
from src.progress.schemas import CourseProgressResponse


async def get_lecture_progress(
    db: AsyncSession, user_id: uuid.UUID, lecture_id: uuid.UUID
) -> LectureProgress | None:
    result = await db.execute(
        select(LectureProgress).where(
            LectureProgress.user_id == user_id,
            LectureProgress.lecture_id == lecture_id,
        )
    )
    return result.scalar_one_or_none()


async def get_course_progress(
    db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID
) -> CourseProgressResponse:
    if not await is_enrolled(db, user_id, course_id):
        raise PermissionDenied()

    total_result = await db.execute(
        select(func.count(Lecture.id))
        .join(Lecture.section)
        .where(Lecture.section.has(course_id=course_id))
    )
    total_lectures = total_result.scalar_one()

    progress_result = await db.execute(
        select(LectureProgress)
        .join(LectureProgress.lecture)
        .join(Lecture.section)
        .where(
            LectureProgress.user_id == user_id,
            Lecture.section.has(course_id=course_id),
        )
    )
    progress_records = progress_result.scalars().all()
    completed = sum(1 for p in progress_records if p.is_completed)

    return CourseProgressResponse(
        course_id=course_id,
        total_lectures=total_lectures,
        completed_lectures=completed,
        progress_percent=round(completed / total_lectures * 100, 1) if total_lectures else 0,
        lecture_progress=progress_records,
    )


async def upsert_progress(
    db: AsyncSession,
    user_id: uuid.UUID,
    lecture_id: uuid.UUID,
    watched_seconds: int,
    is_completed: bool,
) -> LectureProgress:
    existing = await get_lecture_progress(db, user_id, lecture_id)

    if existing:
        existing.watched_seconds = max(existing.watched_seconds, watched_seconds)
        if is_completed and not existing.is_completed:
            existing.is_completed = True
            existing.completed_at = datetime.now(timezone.utc)
        await db.commit()
        await db.refresh(existing)
        return existing

    progress = LectureProgress(
        user_id=user_id,
        lecture_id=lecture_id,
        watched_seconds=watched_seconds,
        is_completed=is_completed,
        completed_at=datetime.now(timezone.utc) if is_completed else None,
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return progress
