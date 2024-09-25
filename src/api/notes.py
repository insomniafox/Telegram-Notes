from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_sqlalchemy_session
from models.users.models import User
from schemas.notes import NoteSchema, CreateNoteSchema, UpdateNoteSchema
from services.notes.notes import NotesService
from services.users.dependencies import get_current_user

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('/', response_model=list[NoteSchema])
async def get_notes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_sqlalchemy_session)
):
    response = await NotesService().get_notes(user_id=current_user.id, db=db)
    return response


@router.get('/{note_id}', response_model=NoteSchema)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_sqlalchemy_session)
):
    response = await NotesService().get_note(note_id=note_id, user_id=current_user.id, db=db)
    return response


@router.post('/', response_model=NoteSchema)
async def create_note(
    request: CreateNoteSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_sqlalchemy_session)
):
    response = await NotesService().create_note(
        title=request.title,
        content=request.content,
        tags=request.tags,
        user=current_user,
        db=db
    )
    return response


@router.put('/{note_id}', response_model=NoteSchema)
async def update_note(
    note_id: int,
    request: UpdateNoteSchema,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_sqlalchemy_session)
):
    response = await NotesService().update_note(
        note_id=note_id,
        update_data=request.dict(exclude_unset=True),
        user_id=current_user.id,
        db=db
    )
    return response


@router.delete('/{note_id}')
async def delete_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_sqlalchemy_session)
):
    await NotesService().delete_note(note_id=note_id, user_id=current_user.id, db=db)
    return {}
