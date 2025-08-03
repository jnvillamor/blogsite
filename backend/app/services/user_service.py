from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserUpdate
from app.schemas.blog_schema import BlogResponse
from app.schemas.shared_schema import PaginatedResponse
from app.repositories.user_respository import UserRepository
from app.repositories.blog_repository import BlogRepository

class UserService:
  def __init__(self, db_session: Session):
    self.user_repository = UserRepository(db_session)
    self.auth_service = AuthService(db_session)
    self.blog_repository = BlogRepository(db_session)
    self.db_session = db_session
    
  def get_user_by_id(self, user_id: str, with_blogs: bool = False) -> User:
    """Retrieve a user by their ID."""
    user = self.user_repository.get_by_id(user_id)

    if with_blogs:
      blogs, total = self.blog_repository.get_by_user(user_id)
      user.blogs = blogs

    if not user:
      raise ValueError("User not found")

    return user

  def get_user_blogs(self, user_id: str, limit: int = 5, offset: int = 0):
    """Retrieve all blogs by a specific user."""
    return self.blog_repository.get_by_user(user_id, limit, offset)

  def update_user(self, current_user: User, user_id: str, user_data: UserUpdate) -> User:
    """Update user information."""
    try:
      user = self.get_user_by_id(user_id)
      
      # Only allow the current user to update their own information
      if not user or current_user.id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this user")
      
      # Update user fields
      updated_user = self.user_repository.update_info(user, user_data)
      self.db_session.commit()
      self.db_session.refresh(updated_user)
      return updated_user
    except Exception as e:
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))