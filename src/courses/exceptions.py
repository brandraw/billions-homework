from src.exceptions import NotFound, PermissionDenied


class CourseNotFound(NotFound):
    DETAIL = "Course not found"


class SectionNotFound(NotFound):
    DETAIL = "Section not found"


class CourseNotPublished(PermissionDenied):
    DETAIL = "Course is not published"
