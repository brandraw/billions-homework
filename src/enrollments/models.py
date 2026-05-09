import uuid
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.courses.models import Course
    from src.payments.models import Payment
    from src.users.models import User


class Enrollment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "enrollments"
    __table_args__ = (sa.UniqueConstraint("user_id", "course_id"),)

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), index=True
    )
    payment_id: Mapped[uuid.UUID | None] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("payments.id"), nullable=True
    )

    student: Mapped["User"] = relationship(back_populates="enrollments")
    course: Mapped["Course"] = relationship(back_populates="enrollments")
    payment: Mapped["Payment | None"] = relationship(back_populates="enrollment")
