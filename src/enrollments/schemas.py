import uuid
from datetime import datetime

from src.courses.schemas import CourseListResponse
from src.schemas import AppBaseModel


class EnrollmentResponse(AppBaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    payment_id: uuid.UUID | None
    created_at: datetime


class EnrollmentDetailResponse(EnrollmentResponse):
    course: CourseListResponse


class EnrollRequest(AppBaseModel):
    course_id: uuid.UUID
