from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_sqlalchemy_session
from models.users.models import User
from schemas.notes import NoteSchema, CreateNoteSchema, UpdateNoteSchema, PaginatedNoteSchema
from services.notes.notes import get_paginated_notes
from services.notes.service import NotesService
from services.users.dependencies import get_current_user

router = APIRouter(prefix='/notes', tags=['notes'])


@router.get('', response_model=PaginatedNoteSchema)
async def get_notes(
    request: Request,
    current_user: User = Depends(get_current_user),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await get_paginated_notes(
        user_id=current_user.id,
        offset=offset,
        limit=limit,
        request=request,
        db=db
    )
    return response


@router.get('/{note_id}', response_model=NoteSchema)
async def get_note(
    note_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await NotesService().get_note(
        note_id=note_id,
        user_id=current_user.id,
        db=db
    )
    return response


@router.post('', response_model=NoteSchema)
async def create_note(
    request_body: CreateNoteSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await NotesService.create_note(
        title=request_body.title,
        content=request_body.content,
        tags=request_body.tags,
        user=current_user,
        db=db
    )
    return response


@router.put('/{note_id}', response_model=NoteSchema)
async def update_note(
    note_id: int,
    request: UpdateNoteSchema,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    response = await NotesService.update_note(
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
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    await NotesService.delete_note(
        note_id=note_id,
        user_id=current_user.id,
        db=db
    )
    return {}
