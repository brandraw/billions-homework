import uuid
from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.auth.exceptions import InvalidCredentials, InvalidToken
from src.auth.models import RefreshToken
from src.auth.schemas import RegisterRequest
from src.config import settings
from src.users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_access_token(user_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXP_MINUTES)
    payload = {"sub": str(user_id), "exp": expire, "type": ACCESS_TOKEN_TYPE}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def create_refresh_token_value(user_id: uuid.UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": REFRESH_TOKEN_TYPE}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALG)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
    except jwt.PyJWTError:
        raise InvalidToken()


async def register(db: AsyncSession, data: RegisterRequest) -> User:
    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=data.role,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate(
    db: AsyncSession, email: str, password: str
) -> tuple[User, str, str]:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.hashed_password):
        raise InvalidCredentials()

    access_token = create_access_token(user.id)
    refresh_token_value = create_refresh_token_value(user.id)

    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS)
    db.add(RefreshToken(user_id=user.id, token=refresh_token_value, expires_at=expire))
    await db.commit()

    return user, access_token, refresh_token_value


async def refresh_tokens(db: AsyncSession, token: str) -> tuple[str, str]:
    payload = decode_token(token)
    if payload.get("type") != REFRESH_TOKEN_TYPE:
        raise InvalidToken()

    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == token,
            RefreshToken.is_revoked.is_(False),
        )
    )
    db_token = result.scalar_one_or_none()
    if not db_token or db_token.expires_at < datetime.now(timezone.utc):
        raise InvalidToken()

    db_token.is_revoked = True

    user_id = uuid.UUID(payload["sub"])
    new_access = create_access_token(user_id)
    new_refresh = create_refresh_token_value(user_id)

    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXP_DAYS)
    db.add(RefreshToken(user_id=user_id, token=new_refresh, expires_at=expire))
    await db.commit()

    return new_access, new_refresh


async def logout(db: AsyncSession, token: str) -> None:
    result = await db.execute(
        select(RefreshToken).where(RefreshToken.token == token)
    )
    db_token = result.scalar_one_or_none()
    if db_token:
        db_token.is_revoked = True
        await db.commit()
