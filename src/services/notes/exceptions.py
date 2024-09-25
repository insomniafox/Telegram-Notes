from fastapi import HTTPException


class NoteServiceException(HTTPException):
    pass
