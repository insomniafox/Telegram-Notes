from enum import Enum as PyEnum

from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Role(PyEnum):
    USER = 'user'
    ADMIN = 'admin'


class User(BaseModel):
    __tablename__ = 'users_user'

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(length=50), unique=True, index=True)
    password = Column(String(length=128), nullable=False)
    first_name = Column(String(length=64), nullable=True)
    last_name = Column(String(length=64), nullable=True)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(Role), nullable=False, default=Role.USER)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    telegram_username = Column(String(length=32), nullable=True)
    telegram_chat_id = Column(String(128), nullable=True)

    notes = relationship('Note', back_populates='user')
    refresh_token = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')
