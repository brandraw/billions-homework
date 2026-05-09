import math
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.courses.exceptions import CourseNotFound, SectionNotFound
from src.courses.models import Course, CourseLevel, CourseStatus, Section
from src.courses.schemas import (
    CourseCreateRequest,
    CourseUpdateRequest,
    SectionCreateRequest,
    SectionUpdateRequest,
)


async def list_courses(
    db: AsyncSession,
    *,
    page: int = 1,
    size: int = 20,
    category: str | None = None,
    level: CourseLevel | None = None,
    search: str | None = None,
) -> tuple[list[Course], int]:
    query = (
        select(Course)
        .where(Course.status == CourseStatus.published)
        .options(selectinload(Course.instructor))
    )

    if category:
        query = query.where(Course.category == category)
    if level:
        query = query.where(Course.level == level)
    if search:
        query = query.where(Course.title.ilike(f"%{search}%"))

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        query.order_by(Course.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    return result.scalars().all(), total


async def get_course(db: AsyncSession, course_id: uuid.UUID) -> Course:
    result = await db.execute(
        select(Course)
        .where(Course.id == course_id)
        .options(
            selectinload(Course.instructor),
            selectinload(Course.sections),
        )
    )
    course = result.scalar_one_or_none()
    if not course:
        raise CourseNotFound()
    return course


async def get_course_for_instructor(
    db: AsyncSession, course_id: uuid.UUID, instructor_id: uuid.UUID
) -> Course:
    course = await get_course(db, course_id)
    if course.instructor_id != instructor_id:
        from src.exceptions import PermissionDenied
        raise PermissionDenied()
    return course


async def create_course(
    db: AsyncSession, instructor_id: uuid.UUID, data: CourseCreateRequest
) -> Course:
    course = Course(
        title=data.title,
        description=data.description,
        thumbnail_url=data.thumbnail_url,
        price=data.price,
        instructor_id=instructor_id,
        category=data.category,
        level=data.level,
    )
    db.add(course)
    await db.commit()
    await db.refresh(course)
    return await get_course(db, course.id)


async def update_course(
    db: AsyncSession, course: Course, data: CourseUpdateRequest
) -> Course:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(course, field, value)
    await db.commit()
    await db.refresh(course)
    return course


async def delete_course(db: AsyncSession, course: Course) -> None:
    await db.delete(course)
    await db.commit()


async def publish_course(db: AsyncSession, course: Course) -> Course:
    course.status = CourseStatus.published
    await db.commit()
    await db.refresh(course)
    return course


async def archive_course(db: AsyncSession, course: Course) -> Course:
    course.status = CourseStatus.archived
    await db.commit()
    await db.refresh(course)
    return course


async def get_section(db: AsyncSession, section_id: uuid.UUID) -> Section:
    result = await db.execute(select(Section).where(Section.id == section_id))
    section = result.scalar_one_or_none()
    if not section:
        raise SectionNotFound()
    return section


async def create_section(
    db: AsyncSession, course_id: uuid.UUID, data: SectionCreateRequest
) -> Section:
    section = Section(course_id=course_id, title=data.title, order=data.order)
    db.add(section)
    await db.commit()
    await db.refresh(section)
    return section


async def update_section(
    db: AsyncSession, section: Section, data: SectionUpdateRequest
) -> Section:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(section, field, value)
    await db.commit()
    await db.refresh(section)
    return section


async def delete_section(db: AsyncSession, section: Section) -> None:
    await db.delete(section)
    await db.commit()
