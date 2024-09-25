from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.base import BaseModel


class RefreshToken(BaseModel):
    __tablename__ = 'tokens_refresh_tokens'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(ForeignKey('users_user.id'), nullable=False)
    token = Column(String(512), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', back_populates='refresh_token')
