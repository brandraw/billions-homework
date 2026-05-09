import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.lectures import service
from src.lectures.models import Lecture


async def get_lecture_or_404(
    lecture_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Lecture:
    return await service.get_lecture(db, lecture_id)
