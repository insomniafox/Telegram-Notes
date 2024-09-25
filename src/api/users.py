from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.database import get_sqlalchemy_session
from models.users.models import User
from schemas.users import UserSchema, UserRegisterSchema, UserLoginSchema, RefreshTokenSchema
from services.auth.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    token_refresh
)
from services.users.dependencies import get_current_user, get_current_admin_user
from services.users.service import UserService
from services.users.utils import register_user

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/register')
async def register(
    request: UserRegisterSchema,
    db: Session = Depends(get_sqlalchemy_session)
):
    user = await register_user(
        login=request.login,
        password=request.password,
        first_name=request.first_name,
        last_name=request.last_name,
        telegram_username=request.telegram_username,
        telegram_chat_id=request.telegram_chat_id,
        db=db
    )
    access_token = await create_access_token({'sub': str(user.id)})
    refresh_token = await create_refresh_token(user=user, data={'sub': str(user.id)}, db=db)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/login')
async def login_user(
    request: UserLoginSchema,
    db: Session = Depends(get_sqlalchemy_session)
):
    user = await authenticate_user(
        login=request.login,
        password=request.password,
        db=db
    )
    access_token = await create_access_token(data={'sub': str(user.id)})
    refresh_token = await create_refresh_token(user=user, data={'sub': str(user.id)}, db=db)
    return {'access_token': access_token, 'refresh_token': refresh_token}


@router.post('/refresh')
async def refresh(
    request: RefreshTokenSchema,
    db: Session = Depends(get_sqlalchemy_session)
):
    response = await token_refresh(refresh_token=request.refresh_token, db=db)
    return response


@router.get('/me', tags=['users'], response_model=UserSchema)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get('/{user_id}', tags=['users'], response_model=UserSchema)
async def get_user(
    user_id: int,
    db: Session = Depends(get_sqlalchemy_session),
    current_user: User = Depends(get_current_admin_user)
):
    user = await UserService().get_user(id=user_id, db=db)
    return user


@router.get('/', tags=['users'], response_model=list[UserSchema])
async def get_user(
    db: Session = Depends(get_sqlalchemy_session),
    current_user: User = Depends(get_current_admin_user)
):
    user = await UserService().get_users(db=db)
    return user
