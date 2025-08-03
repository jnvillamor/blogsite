from sqlalchemy import Column, String, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

class Comment(Base):
  __tablename__ = 'comments'
  
  id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
  blog_id = Column(UUID(as_uuid=True), ForeignKey('blogs.id'), nullable=False)
  author_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
  parent_id = Column(UUID(as_uuid=True), ForeignKey('comments.id'), nullable=True)
  content = Column(String, nullable=False)
  created_at = Column(DateTime, nullable=False, default=func.now())
  updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

  author = relationship('User')
  blog = relationship('Blog', back_populates='comments')
  parent = relationship('Comment', remote_side=[id], back_populates='replies')
  replies = relationship('Comment', back_populates='parent', cascade='all, delete, delete-orphan')
  
  def __repr__(self):
    return f"<Comment(id={self.id}, blog_id={self.blog_id}, author_id={self.author_id}, content='{self.content[:20]}...')>"