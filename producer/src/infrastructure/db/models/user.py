import uuid
from datetime import datetime

from sqlalchemy import Column, String, VARCHAR, DateTime, Boolean, UUID
from sqlalchemy.orm import relationship

from src.infrastructure.db import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(VARCHAR(70), unique=True, nullable=False)
    phone_number = Column(VARCHAR(20), nullable=False)
    phone_number_verified = Column(Boolean, nullable=False, default=False)
    email_verified = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    admin = Column(Boolean, nullable=False, default=False)

    files = relationship("FileModel", back_populates="user")
    cards = relationship("CardModel", back_populates="user", foreign_keys='CardModel.user_id')
    groups = relationship("GroupModel", back_populates="user")
    sharing_urls = relationship("SharingURLModel", back_populates="user")
