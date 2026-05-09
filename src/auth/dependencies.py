import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.constants import ACCESS_TOKEN_TYPE
from src.auth.exceptions import InactiveUser, InvalidToken
from src.auth.service import decode_token
from src.database import get_db
from src.exceptions import PermissionDenied
from src.users.models import User, UserRole

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    payload = decode_token(token)
    if payload.get("type") != ACCESS_TOKEN_TYPE:
        raise InvalidToken()

    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == uuid.UUID(user_id)))
    user = result.scalar_one_or_none()

    if not user:
        raise InvalidToken()
    if not user.is_active:
        raise InactiveUser()

    return user


def require_roles(*roles: UserRole):
    async def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in roles:
            raise PermissionDenied()
        return current_user

    return dependency


require_instructor = require_roles(UserRole.instructor, UserRole.admin)
require_admin = require_roles(UserRole.admin)
