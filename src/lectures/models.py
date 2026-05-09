import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.courses.models import Section
    from src.progress.models import LectureProgress


class Lecture(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lectures"

    section_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("sections.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(sa.String(255))
    video_url: Mapped[str | None] = mapped_column(sa.String(500))
    duration_seconds: Mapped[int | None] = mapped_column(sa.Integer)
    order: Mapped[int] = mapped_column(sa.Integer, default=0)
    is_preview: Mapped[bool] = mapped_column(sa.Boolean, default=False, server_default="false")

    section: Mapped["Section"] = relationship(back_populates="lectures")
    progress_records: Mapped[list["LectureProgress"]] = relationship(back_populates="lecture")
