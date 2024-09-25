from typing import Optional

from fastapi import HTTPException, status


class UserFotFoundException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )


class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User with this login already exists"
        )


class UserHasNoAccess(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "User has no access"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
