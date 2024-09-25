from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from models.base import BaseModel


class Note(BaseModel):
    __tablename__ = 'notes_note'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users_user.id'), nullable=False)
    title = Column(String(64), nullable=False)
    content = Column(Text, nullable=False)
    tags = Column(JSONB, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship('User', back_populates='notes')
