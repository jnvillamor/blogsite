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
  
  def get_by_user(self, user_id: str, limit: int = 5) -> List[Blog]:
    """Retrieve all blogs by a specific user."""
    return self.db_session.query(Blog).filter_by(author_id=user_id).limit(limit).all()