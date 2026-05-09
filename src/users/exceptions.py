from src.exceptions import NotFound


class UserNotFound(NotFound):
    DETAIL = "User not found"
