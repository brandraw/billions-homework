import uuid

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.users import service
from src.users.models import User


async def get_user_or_404(user_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> User:
    return await service.get_by_id(db, user_id)
