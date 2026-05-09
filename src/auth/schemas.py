from pydantic import EmailStr

from src.schemas import AppBaseModel
from src.users.models import UserRole


class RegisterRequest(AppBaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.student


class LoginRequest(AppBaseModel):
    email: EmailStr
    password: str


class TokenResponse(AppBaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(AppBaseModel):
    refresh_token: str


class AccessTokenResponse(AppBaseModel):
    access_token: str
    token_type: str = "bearer"
