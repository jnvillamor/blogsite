from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class User(Base):
  __tablename__ = "users"
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  email = Column(String, unique=True, nullable=False)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  hashed_password = Column(String, nullable=False)
  created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
  updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=False)

  blogs = relationship("Blog", back_populates="author", cascade="all, delete, delete-orphan", passive_deletes=True)

  def __repr__(self):
    return f"<User(id={self.id}, email={self.email}, first_name={self.first_name}, last_name={self.last_name})>"