import uuid
from datetime import datetime
from decimal import Decimal

from src.payments.models import PaymentStatus
from src.schemas import AppBaseModel


class PaymentResponse(AppBaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    course_id: uuid.UUID
    amount: Decimal
    status: PaymentStatus
    payment_method: str
    external_id: str | None
    created_at: datetime


class PaymentCreateRequest(AppBaseModel):
    course_id: uuid.UUID
    payment_method: str


class PaymentConfirmRequest(AppBaseModel):
    external_id: str
