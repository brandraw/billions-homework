import uuid
from datetime import datetime

from src.schemas import AppBaseModel


class LectureProgressResponse(AppBaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    lecture_id: uuid.UUID
    is_completed: bool
    watched_seconds: int
    completed_at: datetime | None
    updated_at: datetime


class CourseProgressResponse(AppBaseModel):
    course_id: uuid.UUID
    total_lectures: int
    completed_lectures: int
    progress_percent: float
    lecture_progress: list[LectureProgressResponse]


class UpdateProgressRequest(AppBaseModel):
    watched_seconds: int
    is_completed: bool = False
