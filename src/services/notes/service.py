from typing import Sequence

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, status

from db.database import get_sqlalchemy_session
from models.notes.models import Note
from models.users.models import User
from services.notes.exceptions import NoteServiceException


class NotesService:
    @classmethod
    async def get_notes(
        cls,
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        **filters
    ) -> Sequence[Note]:
        query = await db.execute(select(Note).filter_by(**filters).limit(limit).offset(offset))
        notes = query.scalars().all()
        return notes

    @classmethod
    async def count_notes(
        cls,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        **filters
    ) -> int:
        total_query = await db.execute(select(func.count()).select_from(Note).filter_by(**filters))
        return total_query.scalar()

    @classmethod
    async def get_note(
        cls,
        note_id: int,
        user_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session),
    ) -> Note:
        result = await db.execute(select(Note).filter_by(id=note_id, user_id=user_id))
        note = result.scalars().first()
        if not note:
            raise NoteServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Note not found.'
            )
        return note

    @classmethod
    async def create_note(
        cls,
        title: str,
        content: str,
        tags: list[str],
        user: User,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> Note:
        note = Note(
            title=title,
            content=content,
            tags=tags,
            user_id=user.id
        )
        db.add(note)
        await db.commit()
        await db.refresh(note)
        return note

    @classmethod
    async def update_note(
        cls,
        note_id: int,
        update_data: dict,
        user_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ):
        note: Note = await cls.get_note(note_id=note_id, user_id=user_id, db=db)
        for key, value in update_data.items():
            setattr(note, key, value)
        await db.commit()
        await db.refresh(note)
        return note

    @classmethod
    async def delete_note(
        cls,
        note_id: int,
        user_id: int,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ):
        note: Note = await cls.get_note(note_id=note_id, user_id=user_id, db=db)
        await db.delete(note)
        await db.commit()
