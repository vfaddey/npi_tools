import uuid
from datetime import datetime

from sqlalchemy import UUID, Column, String, Enum, JSON, DateTime

from app.db.database import Base
from app.entities.card import CardStatus


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    card_type = Column(String, nullable=False, index=True)
    status = Column(Enum(CardStatus), default=CardStatus.PENDING, nullable=False)
    markdown_text = Column(String, nullable=False, default="")
    file_id = Column(UUID(as_uuid=True), nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    result = Column(JSON, default=None)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
