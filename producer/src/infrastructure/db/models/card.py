import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.domain.entities import CardStatus
from src.infrastructure.db import Base


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_type = Column(String, nullable=False, index=True)
    status = Column(Enum(CardStatus), default=CardStatus.PENDING, nullable=False)
    markdown_text = Column(String, nullable=False, default="")
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    result = Column(JSON, default={}, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    user = relationship("UserModel", back_populates="cards")
    file = relationship("FileModel", back_populates="cards")