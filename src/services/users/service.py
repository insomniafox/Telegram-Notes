from typing import Optional, Sequence

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_sqlalchemy_session
from models.users.models import User, Role
from services.auth.utils import get_password_hash
from services.users.exceptions import UserFotFoundException


class UserService:
    async def get_users(
        self,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        **filters
    ) -> Sequence[User]:
        result = await db.execute(select(User).filter_by(**filters))
        return result.scalars().all()

    async def get_user(
        self,
        db: AsyncSession = Depends(get_sqlalchemy_session),
        raise_exception: bool = True,
        **filters
    ) -> User | None:
        result = await db.execute(select(User).filter_by(**filters))
        user = result.scalars().first()
        if not user and raise_exception:
            raise UserFotFoundException
        return user

    async def create_user(
        self,
        login: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role: Optional[str] = None,
        telegram_username: Optional[str] = None,
        telegram_chat_id: Optional[str] = None,
        db: AsyncSession = Depends(get_sqlalchemy_session)
    ) -> User:
        if not role:
            role = Role.USER
        user = User(
            login=login,
            password=get_password_hash(password),
            first_name=first_name,
            last_name=last_name,
            role=role,
            telegram_username=telegram_username,
            telegram_chat_id=telegram_chat_id,
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
