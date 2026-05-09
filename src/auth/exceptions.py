from src.exceptions import DetailedHTTPException
from fastapi import status


class InvalidCredentials(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Invalid email or password"


class InvalidToken(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "Invalid or expired token"


class InactiveUser(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Inactive user account"
