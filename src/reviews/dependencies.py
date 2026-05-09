import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.reviews import service
from src.reviews.models import Review


async def get_review_or_404(
    review_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Review:
    return await service.get_review(db, review_id)
