from sqlalchemy.orm import Session
from typing import List

from app.schemas.blog_schema import BlogCreate
from app.models.blog import Blog

class BlogRepository:
  def __init__(self, db_session: Session):
    self.db_session = db_session
  
  def create(self, blog: BlogCreate) -> Blog:
    try:
      new_blog = Blog(**blog.model_dump())
      self.db_session.add(new_blog)
      self.db_session.commit()
      self.db_session.refresh(new_blog)
      return new_blog
    except Exception as e:
      self.db_session.rollback()
      raise e
  
  def get_by_user(self, user_id: str, limit: int = 5, offset: int = 0) -> List[Blog]:
    """Retrieve all blogs by a specific user."""
    total = self.db_session.query(Blog).filter(Blog.author_id == user_id).count()
    blogs = (
      self.db_session.query(Blog)
      .filter(Blog.author_id == user_id)
      .order_by(Blog.created_at.desc())
      .limit(limit)
      .offset(offset)
      .all()
    )

    return blogs, total
  
  def get_by_id(self, blog_id: str) -> Blog:
    """Retrieve a blog by its ID."""
    return self.db_session.query(Blog).filter(Blog.id == blog_id).first()

  def get_all(self, limit: int = 5, offset: int = 0) -> List[Blog]:
    """Retrieve all blogs with pagination."""
    total = self.db_session.query(Blog).count()
    blogs = (
      self.db_session.query(Blog)
      .order_by(Blog.created_at.desc())
      .limit(limit)
      .offset(offset)
      .all()
    )
    return blogs, total
  
  def update(self, blog: Blog, blog_data: BlogCreate) -> Blog:
    """Update an existing blog post."""
    try:
      for key, value in blog_data.model_dump().items():
        setattr(blog, key, value)
      self.db_session.commit()
      self.db_session.refresh(blog)
      return blog
    except Exception as e:
      self.db_session.rollback()
      raise e
  
  def delete(self, blog: Blog):
    """Delete a blog post."""
    try:
      self.db_session.delete(blog)
      self.db_session.commit()
    except Exception as e:
      self.db_session.rollback()
      raise e