from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permission denied"


class NotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Not found"


class BadRequest(DetailedHTTPException):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST
    DETAIL = "Bad request"


class Conflict(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Conflict"
