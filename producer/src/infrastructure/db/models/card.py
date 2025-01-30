import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, String, Enum, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from src.domain.entities import CardStatus
from src.infrastructure.db import Base


class CardModel(Base):
    __tablename__ = "cards"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    card_type = Column(String, nullable=False, index=True)
    name = Column(String(100), nullable=False, default='', server_default='')
    card_type_translation = Column(String, nullable=True)
    status = Column(Enum(CardStatus), default=CardStatus.CREATED, nullable=False)
    markdown_text = Column(String, nullable=False, default='')
    file_id = Column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="CASCADE"))
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    result = Column(JSON, default={}, nullable=False)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    group = relationship("GroupModel", back_populates="cards")
    user = relationship("UserModel", back_populates="cards")
    file = relationship("FileModel", back_populates="cards")
    sharing_url = relationship("SharingURLModel", back_populates="card")
    copies = relationship("CardCopyModel", back_populates="card")


class SharingURLModel(Base):
    __tablename__ = "sharing_urls"

    card_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=False, index=True)
    base_url = Column(String, nullable=False)
    code = Column(String, nullable=False, unique=True, index=True, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    card = relationship("CardModel", back_populates="sharing_url", lazy="joined")
    user = relationship("UserModel", back_populates="sharing_urls")


class CardCopyModel(Base):
    __tablename__ = "card_copies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    card_id = Column(UUID(as_uuid=True), ForeignKey("cards.id"), nullable=False, index=True)
    copier_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    card = relationship("CardModel", back_populates="copies")
    user = relationship("UserModel")