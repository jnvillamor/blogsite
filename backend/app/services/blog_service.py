from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.blog import Blog
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import BlogCreate

class BlogService:
  def __init__(self, db_session: Session):
    self.db_session = db_session
    self.blog_repository = BlogRepository(db_session)
  
  def create_blog(self, blog_data: BlogCreate, user_id: UUID) -> Blog:
    """Create a new blog post."""
    
    if not blog_data.title or not blog_data.content:
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Title and content are required"
      )
    
    if blog_data.author_id != str(user_id):
      raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You can only create blogs for your own account"
      )
    
    blog = self.blog_repository.create(blog_data)
    return blog
  
  def get_blogs(self, limit: int = 5, offset: int = 0):
    """Get all blogs with pagination."""
    return self.blog_repository.get_all(limit, offset)

  def get_blog_by_id(self, blog_id: str) -> Blog:
    """Get a blog by its ID."""
    blog = self.blog_repository.get_by_id(blog_id)
    if not blog:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    return blog