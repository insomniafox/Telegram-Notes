from typing import Optional

from fastapi import HTTPException, status


class UserHasNoTelegramLinked(HTTPException):
    def __init__(self, detail: Optional[str] = None):
        if not detail:
            detail = "User has no telegram linked"
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )
