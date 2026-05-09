import enum
import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base, TimestampMixin, UUIDMixin

if TYPE_CHECKING:
    from src.courses.models import Course
    from src.enrollments.models import Enrollment
    from src.users.models import User


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    completed = "completed"
    failed = "failed"
    refunded = "refunded"


class Payment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "payments"

    user_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("users.id"), index=True
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        PG_UUID(as_uuid=True), sa.ForeignKey("courses.id"), index=True
    )
    amount: Mapped[Decimal] = mapped_column(sa.Numeric(10, 2))
    status: Mapped[PaymentStatus] = mapped_column(
        sa.Enum(PaymentStatus),
        default=PaymentStatus.pending,
        server_default=PaymentStatus.pending,
    )
    payment_method: Mapped[str] = mapped_column(sa.String(50))
    external_id: Mapped[str | None] = mapped_column(sa.String(255), nullable=True)

    user: Mapped["User"] = relationship(back_populates="payments")
    course: Mapped["Course"] = relationship(back_populates="payments")
    enrollment: Mapped["Enrollment | None"] = relationship(back_populates="payment")
