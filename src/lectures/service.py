import uuid

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.lectures.exceptions import LectureNotFound
from src.lectures.models import Lecture
from src.lectures.schemas import LectureCreateRequest, LectureUpdateRequest


async def get_lecture(db: AsyncSession, lecture_id: uuid.UUID) -> Lecture:
    result = await db.execute(
        select(Lecture)
        .where(Lecture.id == lecture_id)
        .options(selectinload(Lecture.section))
    )
    lecture = result.scalar_one_or_none()
    if not lecture:
        raise LectureNotFound()
    return lecture


async def create_lecture(
    db: AsyncSession, section_id: uuid.UUID, data: LectureCreateRequest
) -> Lecture:
    lecture = Lecture(
        section_id=section_id,
        title=data.title,
        video_url=data.video_url,
        duration_seconds=data.duration_seconds,
        order=data.order,
        is_preview=data.is_preview,
    )
    db.add(lecture)
    await db.commit()
    await db.refresh(lecture)
    return lecture


async def update_lecture(
    db: AsyncSession, lecture: Lecture, data: LectureUpdateRequest
) -> Lecture:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(lecture, field, value)
    await db.commit()
    await db.refresh(lecture)
    return lecture


async def delete_lecture(db: AsyncSession, lecture: Lecture) -> None:
    await db.delete(lecture)
    await db.commit()
