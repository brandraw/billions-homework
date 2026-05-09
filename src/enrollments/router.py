import math

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_db
from src.enrollments import service
from src.enrollments.dependencies import get_enrollment_or_404
from src.enrollments.exceptions import EnrollmentNotFound
from src.enrollments.models import Enrollment
from src.enrollments.schemas import EnrollmentDetailResponse, EnrollmentResponse, EnrollRequest
from src.exceptions import PermissionDenied
from src.schemas import PaginatedResponse
from src.users.models import User

router = APIRouter()


@router.get("", response_model=PaginatedResponse[EnrollmentDetailResponse])
async def list_my_enrollments(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    enrollments, total = await service.get_user_enrollments(
        db, current_user.id, page=page, size=size
    )
    return PaginatedResponse(
        items=enrollments,
        total=total,
        page=page,
        size=size,
        pages=math.ceil(total / size) if total else 0,
    )


@router.post("", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
async def enroll(
    data: EnrollRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.enroll_free(db, current_user.id, data.course_id)


@router.delete("/{enrollment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unenroll(
    enrollment: Enrollment = Depends(get_enrollment_or_404),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if enrollment.user_id != current_user.id:
        raise PermissionDenied()
    await service.unenroll(db, enrollment)
