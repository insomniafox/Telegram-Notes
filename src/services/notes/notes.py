from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import Depends, status

from db.database import get_sqlalchemy_session
from models.notes.models import Note
from models.users.models import User
from services.notes.exceptions import NoteServiceException


class NotesService:
    async def get_notes(
        self,
        db: Session = Depends(get_sqlalchemy_session),
        **filters
    ) -> list[Note]:
        query = await db.execute(select(Note).filter_by(**filters))
        notes = query.scalars().all()
        return notes

    async def get_note(
        self,
        note_id: int,
        user_id: int,
        db: Session = Depends(get_sqlalchemy_session),
    ) -> Note:
        result = await db.execute(select(Note).filter_by(id=note_id, user_id=user_id))
        note = result.scalars().first()
        if not note:
            raise NoteServiceException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Note not found.'
            )
        return note

    async def create_note(
        self,
        title: str,
        content: str,
        tags: list[str],
        user: User,
        db: Session = Depends(get_sqlalchemy_session)
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

    async def update_note(
        self,
        note_id: int,
        update_data: dict,
        user_id: int,
        db: Session = Depends(get_sqlalchemy_session)
    ):
        note: Note = await self.get_note(note_id=note_id, user_id=user_id, db=db)
        for key, value in update_data.items():
            setattr(note, key, value)
        await db.commit()
        await db.refresh(note)
        return note

    async def delete_note(
        self,
        note_id: int,
        user_id: int,
        db: Session = Depends(get_sqlalchemy_session)
    ):
        note: Note = await self.get_note(note_id=note_id, user_id=user_id, db=db)
        await db.delete(note)
        await db.commit()
