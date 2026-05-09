import math
import uuid

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_db
from src.exceptions import PermissionDenied
from src.reviews import service
from src.reviews.dependencies import get_review_or_404
from src.reviews.models import Review
from src.reviews.schemas import ReviewCreateRequest, ReviewResponse, ReviewUpdateRequest
from src.schemas import PaginatedResponse
from src.users.models import User

router = APIRouter()


@router.get("/courses/{course_id}/reviews", response_model=PaginatedResponse[ReviewResponse])
async def list_reviews(
    course_id: uuid.UUID,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    reviews, total = await service.get_course_reviews(db, course_id, page=page, size=size)
    return PaginatedResponse(
        items=reviews,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


@router.post(
    "/courses/{course_id}/reviews",
    response_model=ReviewResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_review(
    course_id: uuid.UUID,
    data: ReviewCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.create_review(db, current_user.id, course_id, data)


@router.patch("/reviews/{review_id}", response_model=ReviewResponse)
async def update_review(
    data: ReviewUpdateRequest,
    review: Review = Depends(get_review_or_404),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if review.user_id != current_user.id:
        raise PermissionDenied()
    return await service.update_review(db, review, data)


@router.delete("/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_review(
    review: Review = Depends(get_review_or_404),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if review.user_id != current_user.id:
        raise PermissionDenied()
    await service.delete_review(db, review)
