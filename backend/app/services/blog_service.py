from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.blog import Blog
from app.repositories.blog_repository import BlogRepository
from app.schemas.blog_schema import BlogCreate, BlogResponse
from app.schemas.shared_schema import PaginatedResponse

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
  
  def get_blogs(self, limit: int = 5, offset: int = 0) -> PaginatedResponse[BlogResponse]:
    """Get all blogs with pagination."""
    blogs, total = self.blog_repository.get_all(limit, offset)
    return PaginatedResponse[BlogResponse](
      items=blogs,
      total=total,
      limit=limit,
      offset=offset
    )
      