from src.exceptions import Conflict, NotFound


class AlreadyEnrolled(Conflict):
    DETAIL = "Already enrolled in this course"


class EnrollmentNotFound(NotFound):
    DETAIL = "Enrollment not found"


class CourseIsPaid(Conflict):
    DETAIL = "This course requires payment to enroll"
