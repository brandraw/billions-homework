import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.courses import service
from src.courses.models import Course, Section
from src.database import get_db


async def get_course_or_404(
    course_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Course:
    return await service.get_course(db, course_id)


async def get_section_or_404(
    section_id: uuid.UUID, db: AsyncSession = Depends(get_db)
) -> Section:
    return await service.get_section(db, section_id)
