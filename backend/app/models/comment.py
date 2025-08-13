from sqlalchemy import Column, String, ForeignKey, DateTime, Table, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.db.base import Base

comment_likes = Table(
  "comment_likes",
  Base.metadata,
  Column("user_id", UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
  Column("comment_id", UUID(as_uuid=True), ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True),
  UniqueConstraint('user_id', 'comment_id', name='unique_user_comment_like'),
)

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
  liked_by = relationship(
    "User", 
    secondary=comment_likes, 
    back_populates="liked_comments", 
    passive_deletes=True
  )
  
  def __repr__(self):
    return f"<Comment(id={self.id}, blog_id={self.blog_id}, author_id={self.author_id}, content='{self.content[:20]}...')>"