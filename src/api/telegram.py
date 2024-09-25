from urllib.parse import quote

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.database import get_sqlalchemy_session
from models.users.models import User
from schemas.telegram import SetTelegramIdSchema
from schemas.users import UserSchema
from services.telegram.telegram import TelegramService
from services.users.dependencies import get_current_user

router = APIRouter(prefix='/telegram', tags=['telegram'])


@router.get('/get_token')
async def get_telegram_link_token(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_sqlalchemy_session)
):
    token = await TelegramService().set_telegram_link_token(user=current_user, db=db)
    response = f'https://t.me/{settings.TELEGRAM_BOT_USERNAME}?start={quote(token)}'
    return response


@router.post('/set_telegram_id')
async def set_telegram_id(
    request: SetTelegramIdSchema,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> UserSchema:
    user = await TelegramService().set_user_telegram_id(
        token=request.token,
        telegram_id=request.telegram_id,
        db=db
    )
    return user


@router.post('/auth')
async def telegram_bot_auth(
    telegram_id: str | int,
    current_user: User = Depends(get_current_user)
):
    response = await TelegramService().get_telegram_access_token(current_user, telegram_id)
    return response
