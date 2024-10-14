from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request
from services.notes.service import NotesService


async def get_paginated_notes(
    db: AsyncSession,
    request: Request,
    user_id: int,
    offset: Optional[int] = 10,
    limit: Optional[int] = 10,
    **filters
) -> dict:
    notes = await NotesService.get_notes(
        user_id=user_id,
        limit=limit,
        offset=offset,
        db=db,
    )
    total_count = await NotesService.count_notes(db=db)

    base_url = str(request.url.remove_query_params(("offset", "limit")))
    next_url = f"{base_url}?limit={limit}&offset={offset + limit}" if offset + limit < total_count else None
    previous_url = f"{base_url}?limit={limit}&offset={max(0, offset - limit)}" if offset > 0 else None

    response = {
        'count': total_count,
        'next': next_url,
        'previous': previous_url,
        'result': notes
    }
    return response
