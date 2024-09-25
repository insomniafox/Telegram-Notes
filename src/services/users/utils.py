from typing import Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_sqlalchemy_session
from models.users.models import User
from services.users.exceptions import UserAlreadyExistsException
from services.users.service import UserService


async def register_user(
    login: str,
    password: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    role: Optional[str] = None,
    telegram_username: Optional[str] = None,
    telegram_chat_id: Optional[str] = None,
    db: AsyncSession = Depends(get_sqlalchemy_session)
) -> User:
    user = await UserService().get_user(login=login, db=db, raise_exception=False)
    if user:
        raise UserAlreadyExistsException
    user = await UserService().create_user(
        login=login,
        password=password,
        first_name=first_name,
        last_name=last_name,
        role=role,
        telegram_username=telegram_username,
        telegram_chat_id=telegram_chat_id,
        db=db
    )
    return user
