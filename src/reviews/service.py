import math
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from src.enrollments.service import is_enrolled
from src.reviews.exceptions import AlreadyReviewed, NotEnrolled, ReviewNotFound
from src.reviews.models import Review
from src.reviews.schemas import ReviewCreateRequest, ReviewUpdateRequest


async def get_review(db: AsyncSession, review_id: uuid.UUID) -> Review:
    result = await db.execute(
        select(Review)
        .where(Review.id == review_id)
        .options(selectinload(Review.user))
    )
    review = result.scalar_one_or_none()
    if not review:
        raise ReviewNotFound()
    return review


async def get_course_reviews(
    db: AsyncSession, course_id: uuid.UUID, *, page: int = 1, size: int = 20
) -> tuple[list[Review], int]:
    query = (
        select(Review)
        .where(Review.course_id == course_id)
        .options(selectinload(Review.user))
    )

    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar_one()

    result = await db.execute(
        query.order_by(Review.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    return result.scalars().all(), total


async def get_average_rating(db: AsyncSession, course_id: uuid.UUID) -> float:
    result = await db.execute(
        select(func.avg(Review.rating)).where(Review.course_id == course_id)
    )
    avg = result.scalar_one()
    return round(float(avg), 1) if avg else 0.0


async def create_review(
    db: AsyncSession,
    user_id: uuid.UUID,
    course_id: uuid.UUID,
    data: ReviewCreateRequest,
) -> Review:
    if not await is_enrolled(db, user_id, course_id):
        raise NotEnrolled()

    existing = await db.execute(
        select(Review).where(Review.user_id == user_id, Review.course_id == course_id)
    )
    if existing.scalar_one_or_none():
        raise AlreadyReviewed()

    review = Review(
        user_id=user_id,
        course_id=course_id,
        rating=data.rating,
        content=data.content,
    )
    db.add(review)
    await db.commit()
    await db.refresh(review)
    return await get_review(db, review.id)


async def update_review(
    db: AsyncSession, review: Review, data: ReviewUpdateRequest
) -> Review:
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(review, field, value)
    await db.commit()
    await db.refresh(review)
    return review


async def delete_review(db: AsyncSession, review: Review) -> None:
    await db.delete(review)
    await db.commit()
