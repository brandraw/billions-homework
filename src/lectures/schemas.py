import uuid
from datetime import datetime

from src.schemas import AppBaseModel


class LectureResponse(AppBaseModel):
    id: uuid.UUID
    section_id: uuid.UUID
    title: str
    video_url: str | None
    duration_seconds: int | None
    order: int
    is_preview: bool
    created_at: datetime


class LectureCreateRequest(AppBaseModel):
    title: str
    video_url: str | None = None
    duration_seconds: int | None = None
    order: int = 0
    is_preview: bool = False


class LectureUpdateRequest(AppBaseModel):
    title: str | None = None
    video_url: str | None = None
    duration_seconds: int | None = None
    order: int | None = None
    is_preview: bool | None = None
