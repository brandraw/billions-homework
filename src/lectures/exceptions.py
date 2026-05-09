from src.exceptions import NotFound, PermissionDenied


class LectureNotFound(NotFound):
    DETAIL = "Lecture not found"


class LectureAccessDenied(PermissionDenied):
    DETAIL = "You must be enrolled to access this lecture"
