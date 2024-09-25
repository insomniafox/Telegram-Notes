from sqlalchemy.orm import Session
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt, ExpiredSignatureError

from db.database import get_sqlalchemy_session
from services.auth.exceptions import (
    TokenExpiredException,
    InvalidTokenException,
    NotAuthorizedException
)

from core.config import settings
from models.users.models import User, Role
from services.auth.utils import ACCESS_TYPE
from services.users.exceptions import UserHasNoAccess
from services.users.service import UserService


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_sqlalchemy_session)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise InvalidTokenException

    token_type = payload.get("type")
    if token_type != ACCESS_TYPE:
        raise InvalidTokenException

    user_id = payload.get("sub")
    if not user_id:
        raise NotAuthorizedException

    user = await UserService().get_user(id=int(user_id), db=db)
    return user


async def get_current_admin_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_sqlalchemy_session)
) -> User:
    user = await get_current_user(token, db)

    if user.role != Role.ADMIN:
        raise UserHasNoAccess

    return user
