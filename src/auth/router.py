from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import service
from src.auth.schemas import (
    AccessTokenResponse,
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
)
from src.database import get_db
from src.exceptions import Conflict
from src.users.models import User
from src.users.schemas import UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise Conflict()
    user = await service.register(db, data)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: LoginRequest, db: AsyncSession = Depends(get_db)):
    _, access_token, refresh_token = await service.authenticate(db, data.email, data.password)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    access_token, refresh_token = await service.refresh_tokens(db, data.refresh_token)
    return AccessTokenResponse(access_token=access_token)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(data: RefreshRequest, db: AsyncSession = Depends(get_db)):
    await service.logout(db, data.refresh_token)
