from src.exceptions import Conflict, NotFound, PermissionDenied


class ReviewNotFound(NotFound):
    DETAIL = "Review not found"


class AlreadyReviewed(Conflict):
    DETAIL = "You have already reviewed this course"


class NotEnrolled(PermissionDenied):
    DETAIL = "You must be enrolled to review this course"
