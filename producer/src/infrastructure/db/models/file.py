import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship, foreign

from src.infrastructure.db import Base


class FileModel(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    filename = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.now)

    user = relationship('UserModel', back_populates='files')
    cards = relationship('CardModel', back_populates='file')