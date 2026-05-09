import uuid
from datetime import datetime
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.lectures.models import Lecture
    from src.users.models import User


class LectureProgress(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "lecture_progress"
    __table_args__ = (sa.UniqueConstraint("user_id", "lecture_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    lecture_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("lectures.id", ondelete="CASCADE"), index=True
    )
    is_completed: Mapped[bool] = mapped_column(sa.Boolean, default=False, server_default="false")
    watched_seconds: Mapped[int] = mapped_column(sa.Integer, default=0, server_default="0")
    completed_at: Mapped[datetime | None] = mapped_column(
        sa.DateTime(timezone=True), nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="progress_records")
    lecture: Mapped["Lecture"] = relationship(back_populates="progress_records")
