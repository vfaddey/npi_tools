import uuid
from datetime import datetime

from sqlalchemy import Column, UUID, DateTime, Boolean, String

from app.db.database import Base


class FileModel(Base):
    __tablename__ = 'files'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    filename = Column(String, nullable=False)
    is_public = Column(Boolean, nullable=False, default=False)
    uploaded_by_user = Column(Boolean, nullable=False)
    uploaded_at = Column(DateTime, nullable=False, default=datetime.now)
