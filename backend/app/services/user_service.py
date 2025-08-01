from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.services.auth_service import AuthService
from app.services.blog_service import BlogService
from app.schemas.user_schema import UserUpdate
from app.repositories.user_respository import UserRepository

class UserService:
  def __init__(self, db_session: Session):
    self.user_repository = UserRepository(db_session)
    self.auth_service = AuthService(db_session)
    self.blog_service = BlogService(db_session)
    self.db_session = db_session
    
  def get_user_by_id(self, user_id: str, with_blogs: bool = False) -> User:
    """Retrieve a user by their ID."""
    user = self.user_repository.get_by_id(user_id)

    if with_blogs:
      user.blogs = self.blog_service.get_user_blogs(user_id)

    if not user:
      raise ValueError("User not found")

    return user
  
  def update_user(self, current_user: User, user_id: str, user_data: UserUpdate) -> User:
    """Update user information."""
    user = self.get_user_by_id(user_id)
    
    # Only allow the current user to update their own information
    if not user or current_user.id != user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to update this user")
    
    # Update user fields
    updated_user = self.user_repository.update_info(user, user_data)
    
    self.db_session.commit()
    return updated_user