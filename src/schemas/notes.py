from datetime import datetime
from typing import Optional

from pydantic import BaseModel, field_validator

from schemas.users import UserSchema


class BaseNoteSchema(BaseModel):
    title: str
    content: str
    tags: list[str]

    @field_validator("tags", mode="before")
    def strip_tags(cls, v):
        if isinstance(v, list):
            return [tag.strip() for tag in v]
        raise ValueError("Tags must be a list of strings")


class CreateNoteSchema(BaseNoteSchema):
    ...


class UpdateNoteSchema(BaseNoteSchema):
    ...


class NoteSchema(BaseNoteSchema):
    id: int
    created_at: datetime
    updated_at: datetime | None
    user: UserSchema

    class Config:
        from_attributes = True


class PaginatedNoteSchema(BaseModel):
    count: int
    next: Optional[str] = None
    previous: Optional[str] = None
    result: list[NoteSchema]
