import uuid
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.courses.models import Course
from src.enrollments import service as enrollment_service
from src.exceptions import BadRequest, NotFound
from src.payments.models import Payment, PaymentStatus


async def get_payment(db: AsyncSession, payment_id: uuid.UUID) -> Payment:
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalar_one_or_none()
    if not payment:
        raise NotFound()
    return payment


async def get_user_payments(db: AsyncSession, user_id: uuid.UUID) -> list[Payment]:
    result = await db.execute(
        select(Payment)
        .where(Payment.user_id == user_id)
        .order_by(Payment.created_at.desc())
    )
    return result.scalars().all()


async def create_payment(
    db: AsyncSession,
    user_id: uuid.UUID,
    course_id: uuid.UUID,
    payment_method: str,
) -> Payment:
    result = await db.execute(select(Course).where(Course.id == course_id))
    course = result.scalar_one_or_none()
    if not course:
        raise NotFound()

    if course.price <= 0:
        raise BadRequest()

    payment = Payment(
        user_id=user_id,
        course_id=course_id,
        amount=course.price,
        payment_method=payment_method,
    )
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


async def confirm_payment(
    db: AsyncSession, payment: Payment, external_id: str
) -> Payment:
    if payment.status != PaymentStatus.pending:
        raise BadRequest()

    payment.status = PaymentStatus.completed
    payment.external_id = external_id
    await db.commit()

    await enrollment_service.enroll_with_payment(
        db, payment.user_id, payment.course_id, payment.id
    )

    await db.refresh(payment)
    return payment
