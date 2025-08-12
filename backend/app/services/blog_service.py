from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from app.db.base import SessionDep
from app.models.blog import Blog
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import BlogCreate, BlogUpdate

class BlogService:
  def __init__(self, db_session: Session):
    self.db_session = db_session
    self.blog_repository = BlogRepository(db_session)
  
  def create_blog(self, blog_data: BlogCreate, user_id: str) -> Blog:
    try:
      """Create a new blog post."""
      self._validate_blog_data(blog_data)     

      if blog_data.author_id != user_id:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="You can only create blogs for your own account"
        )
      
      blog = self.blog_repository.create(blog_data)
      self.db_session.commit()
      self.db_session.refresh(blog)
      return blog
    except Exception as e:
      print(f"Error creating blog: {e}")
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  def get_blogs(self, limit: int = 5, offset: int = 0):
    """Get all blogs with pagination."""
    return self.blog_repository.get_all(limit, offset)

  def get_blog_or_404(self, blog_id: str) -> Blog:
    """Get a blog by its ID."""
    blog = self.blog_repository.get_by_id(blog_id)
    if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog
  
  def update_blog(self, blog_id: str, blog_data: BlogUpdate, user_id: str) -> Blog:
    try:
      """Update an existing blog post."""
      blog = self.get_blog_or_404(blog_id)
      
      self._validate_blog_data(blog_data)     

      if blog_data.author_id != user_id:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="You can only update blogs for your own account"
        )

      updated_blog = self.blog_repository.update(blog, blog_data)
      self.db_session.commit()
      self.db_session.refresh(updated_blog)
      return updated_blog
    except HTTPException as http_exc:
      self.db_session.rollback()
      raise http_exc
    except Exception as e:
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

  def delete_blog(self, blog_id: str, user_id: str) -> dict:
    """Delete a blog post."""
    try:
      blog = self.get_blog_or_404(blog_id)
      
      if str(blog.author_id) != user_id:
        raise HTTPException(
          status_code=status.HTTP_401_UNAUTHORIZED,
          detail="You can only delete blogs for your own account"
        )
      
      self.blog_repository.delete(blog)
      self.db_session.commit()
      return {"detail": "Blog deleted successfully"}
    except HTTPException as http_exc:
      self.db_session.rollback()
      raise http_exc
    except Exception as e:
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  def _validate_blog_data(self, data: BlogCreate) -> None:
    """Validate the blog data."""
    for key, value in data.model_dump().items():
      if value is None:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{key} is required"
        )

# Dependency injection for database session
def get_blog_service(db_session: SessionDep):
  return BlogService(db_session)

BlogServiceDep = Annotated[BlogService, Depends(get_blog_service)]