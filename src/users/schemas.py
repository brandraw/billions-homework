import uuid
from datetime import datetime

from pydantic import EmailStr

from src.schemas import AppBaseModel
from src.users.models import UserRole


class UserResponse(AppBaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime


class UserUpdateRequest(AppBaseModel):
    full_name: str | None = None
    password: str | None = None
