import enum
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.auth.models import RefreshToken
    from src.courses.models import Course
    from src.enrollments.models import Enrollment
    from src.payments.models import Payment
    from src.progress.models import LectureProgress
    from src.reviews.models import Review


class UserRole(str, enum.Enum):
    student = "student"
    instructor = "instructor"
    admin = "admin"


class User(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(sa.String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(sa.String(255))
    full_name: Mapped[str] = mapped_column(sa.String(255))
    role: Mapped[UserRole] = mapped_column(
        sa.Enum(UserRole), default=UserRole.student, server_default=UserRole.student
    )
    is_active: Mapped[bool] = mapped_column(sa.Boolean, default=True, server_default="true")

    courses: Mapped[list["Course"]] = relationship(
        back_populates="instructor", foreign_keys="Course.instructor_id"
    )
    enrollments: Mapped[list["Enrollment"]] = relationship(back_populates="student")
    payments: Mapped[list["Payment"]] = relationship(back_populates="user")
    reviews: Mapped[list["Review"]] = relationship(back_populates="user")
    refresh_tokens: Mapped[list["RefreshToken"]] = relationship(back_populates="user")
    progress_records: Mapped[list["LectureProgress"]] = relationship(back_populates="user")
