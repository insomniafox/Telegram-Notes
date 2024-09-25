from datetime import datetime, timedelta

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.database import get_sqlalchemy_session
from models.users.models import User
from services.auth.auth import create_access_token
from services.telegram.exceptions import UserHasNoTelegramLinked
from services.telegram.utils import generate_token
from services.users.exceptions import UserHasNoAccess
from services.users.service import UserService


class TelegramService:
    async def set_telegram_link_token(
        self,
        user: User,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> str:
        token = generate_token()
        while await UserService().get_user(telegram_link_token=token, raise_exception=False, db=db):
            token = generate_token()
        user.telegram_link_token = token
        await db.commit()
        await db.refresh(user)
        return token

    async def set_user_telegram_id(
        self,
        token: str,
        telegram_id: int | str,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> User:
        user = await UserService().get_user(telegram_link_token=token, db=db)
        user.telegram_id = str(telegram_id)
        await db.commit()
        await db.refresh(user)
        return user

    async def get_telegram_access_token(self, user: User, telegram_id: int | str) -> dict:
        if not user.telegram_id:
            raise UserHasNoTelegramLinked
        if user.telegram_id != telegram_id:
            raise UserHasNoAccess
        expire = datetime.utcnow() + timedelta(minutes=settings.TELEGRAM_ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = await create_access_token(data={'sub': str(user.id)}, expire=expire)
        return {'access_token': access_token}
