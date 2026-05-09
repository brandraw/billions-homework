import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.payments import service
from src.payments.models import Payment


async def get_payment_or_404(
    payment_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Payment:
    return await service.get_payment(db, payment_id)
