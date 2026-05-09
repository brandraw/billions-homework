import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.progress import service
from src.progress.models import LectureProgress


async def get_progress_or_none(
    lecture_id: uuid.UUID,
    user_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
) -> LectureProgress | None:
    return await service.get_lecture_progress(db, user_id, lecture_id)
