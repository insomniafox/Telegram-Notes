from fastapi import HTTPException, status


class TokenExpiredException(HTTPException):
    def __init__(self, detail: str | None = None):
        if not detail:
            detail = "Token expired"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class InvalidTokenException(HTTPException):
    def __init__(self, detail: str | None = None):
        if not detail:
            detail = "Invalid token format"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )


class NotAuthorizedException(HTTPException):
    def __init__(self, detail: str | None = None):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
