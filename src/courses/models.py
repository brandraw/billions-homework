import enum
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.enrollments.models import Enrollment
    from src.lectures.models import Lecture
    from src.payments.models import Payment
    from src.reviews.models import Review
    from src.users.models import User


class CourseLevel(str, enum.Enum):
    beginner = "beginner"
    intermediate = "intermediate"
    advanced = "advanced"


class CourseStatus(str, enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


class Course(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "courses"

    title: Mapped[str] = mapped_column(sa.String(255))
    description: Mapped[str] = mapped_column(sa.Text)
    thumbnail_url: Mapped[str | None] = mapped_column(sa.String(500))
    price: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2), default=0, server_default="0")
    instructor_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    category: Mapped[str] = mapped_column(sa.String(100))
    level: Mapped[CourseLevel] = mapped_column(
        sa.Enum(CourseLevel), default=CourseLevel.beginner, server_default=CourseLevel.beginner
    )
    status: Mapped[CourseStatus] = mapped_column(
        sa.Enum(CourseStatus), default=CourseStatus.draft, server_default=CourseStatus.draft
    )

    instructor: Mapped["User"] = relationship(
        back_populates="courses", foreign_keys=[instructor_id]
    )
    sections: Mapped[list["Section"]] = relationship(
        back_populates="course",
        cascade="all, delete-orphan",
        order_by="Section.order",
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="course")
    payments: Mapped[list["Payment"]] = relationship(back_populates="course")
    reviews: Mapped[list["Review"]] = relationship(back_populates="course")


class Section(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sections"

    course_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("courses.id", ondelete="CASCADE"), index=True
    )
    title: Mapped[str] = mapped_column(sa.String(255))
    order: Mapped[int] = mapped_column(sa.Integer, default=0)

    course: Mapped["Course"] = relationship(back_populates="sections")
    lectures: Mapped[list["Lecture"]] = relationship(
        back_populates="section",
        cascade="all, delete-orphan",
        order_by="Lecture.order",
    )
