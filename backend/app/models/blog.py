from sqlalchemy import Column, String, Text, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class Blog(Base):
  __tablename__ = 'blogs'
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  title = Column(String(255), nullable=False)
  content = Column(Text, nullable=False)
  author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

  author = relationship("User", back_populates="blogs", foreign_keys='Blog.author_id')