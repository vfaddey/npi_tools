import uuid
from datetime import datetime

from sqlalchemy import Column, String, UUID, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship

from src.infrastructure.db import Base


class GroupModel(Base):
    __tablename__ = "groups"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    order = Column(Integer, nullable=False, default=0, server_default='0')

    created_at = Column(DateTime, nullable=False, default=datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    cards = relationship("CardModel", back_populates="group", order_by='CardModel.order', lazy="joined")
    user = relationship("UserModel", back_populates="groups")