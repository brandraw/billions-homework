from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependencies import get_current_user
from src.database import get_db
from src.exceptions import PermissionDenied
from src.payments import service
from src.payments.dependencies import get_payment_or_404
from src.payments.models import Payment
from src.payments.schemas import PaymentConfirmRequest, PaymentCreateRequest, PaymentResponse
from src.users.models import User

router = APIRouter()


@router.get("", response_model=list[PaymentResponse])
async def list_my_payments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.get_user_payments(db, current_user.id)


@router.post("", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
async def create_payment(
    data: PaymentCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await service.create_payment(db, current_user.id, data.course_id, data.payment_method)


@router.get("/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment: Payment = Depends(get_payment_or_404),
    current_user: User = Depends(get_current_user),
):
    if payment.user_id != current_user.id:
        raise PermissionDenied()
    return payment


@router.post("/{payment_id}/confirm", response_model=PaymentResponse)
async def confirm_payment(
    data: PaymentConfirmRequest,
    payment: Payment = Depends(get_payment_or_404),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if payment.user_id != current_user.id:
        raise PermissionDenied()
    return await service.confirm_payment(db, payment, data.external_id)
