import math
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.enrollments.exceptions import AlreadyEnrolled, CourseIsPaid, EnrollmentNotFound
from src.enrollments.models import Enrollment
from src.courses.models import Course


async def is_enrolled(db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID) -> bool:
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )
    )
    return result.scalar_one_or_none() is not None


async def get_enrollment(
    db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID
) -> Enrollment | None:
    result = await db.execute(
        select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )
    )
    return result.scalar_one_or_none()


async def get_enrollment_by_id(db: AsyncSession, enrollment_id: uuid.UUID) -> Enrollment:
    result = await db.execute(
        select(Enrollment)
        .where(Enrollment.id == enrollment_id)
        .options(selectinload(Enrollment.course).selectinload(Course.instructor))
    )
    enrollment = result.scalar_one_or_none()
    if not enrollment:
        raise EnrollmentNotFound()
    return enrollment


async def get_user_enrollments(
    db: AsyncSession, user_id: uuid.UUID, *, page: int = 1, size: int = 20
) -> tuple[list[Enrollment], int]:
    query = (
        select(Enrollment)
        .where(Enrollment.user_id == user_id)
        .options(selectinload(Enrollment.course).selectinload(Course.instructor))
    )

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        query.order_by(Enrollment.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    return result.scalars().all(), total


async def enroll_free(
    db: AsyncSession, user_id: uuid.UUID, course_id: uuid.UUID
) -> Enrollment:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()

    if course and course.price > 0:
        raise CourseIsPaid()

    if await is_enrolled(db, user_id, course_id):
        raise AlreadyEnrolled()

    enrollment = Enrollment(user_id=user_id, course_id=course_id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


async def enroll_with_payment(
    db: AsyncSession,
    user_id: uuid.UUID,
    course_id: uuid.UUID,
    payment_id: uuid.UUID,
) -> Enrollment:
    if await is_enrolled(db, user_id, course_id):
        raise AlreadyEnrolled()

    enrollment = Enrollment(user_id=user_id, course_id=course_id, payment_id=payment_id)
    db.add(enrollment)
    await db.commit()
    await db.refresh(enrollment)
    return enrollment


async def unenroll(db: AsyncSession, enrollment: Enrollment) -> None:
    await db.delete(enrollment)
    await db.commit()
