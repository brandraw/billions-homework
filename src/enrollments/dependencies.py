import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.enrollments import service
from src.enrollments.models import Enrollment


async def get_enrollment_or_404(
    enrollment_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Enrollment:
    return await service.get_enrollment_by_id(db, enrollment_id)
