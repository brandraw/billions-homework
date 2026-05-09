import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import field_validator

from src.courses.models import CourseLevel, CourseStatus
from src.schemas import AppBaseModel


class SectionResponse(AppBaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    title: str
    order: int
    created_at: datetime


class SectionCreateRequest(AppBaseModel):
    title: str
    order: int = 0


class SectionUpdateRequest(AppBaseModel):
    title: str | None = None
    order: int | None = None


class CourseInstructorResponse(AppBaseModel):
    id: uuid.UUID
    full_name: str


class CourseListResponse(AppBaseModel):
    id: uuid.UUID
    title: str
    thumbnail_url: str | None
    price: Decimal
    category: str
    level: CourseLevel
    status: CourseStatus
    instructor: CourseInstructorResponse
    created_at: datetime


class CourseDetailResponse(CourseListResponse):
    description: str
    sections: list[SectionResponse]


class CourseCreateRequest(AppBaseModel):
    title: str
    description: str
    thumbnail_url: str | None = None
    price: Decimal = Decimal("0")
    category: str
    level: CourseLevel = CourseLevel.beginner

    @field_validator("price")
    @classmethod
    def price_must_be_non_negative(cls, v: Decimal) -> Decimal:
        if v < 0:
            raise ValueError("Price must be non-negative")
        return v


class CourseUpdateRequest(AppBaseModel):
    title: str | None = None
    description: str | None = None
    thumbnail_url: str | None = None
    price: Decimal | None = None
    category: str | None = None
    level: CourseLevel | None = None
