import uuid
from datetime import datetime

from pydantic import field_validator

from src.schemas import AppBaseModel


class ReviewUserResponse(AppBaseModel):
    id: uuid.UUID
    full_name: str


class ReviewResponse(AppBaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    rating: int
    content: str
    user: ReviewUserResponse
    created_at: datetime
    updated_at: datetime


class ReviewCreateRequest(AppBaseModel):
    rating: int
    content: str

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: int) -> int:
        if not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewUpdateRequest(AppBaseModel):
    rating: int | None = None
    content: str | None = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v: int | None) -> int | None:
        if v is not None and not 1 <= v <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return v
