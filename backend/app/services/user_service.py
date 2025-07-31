from app.models.user import User
from app.services.auth_service import AuthService
from app.repositories.user_respository import UserRepository
from sqlalchemy.orm import Session

class UserService:
  def __init__(self, db_session: Session):
    self.user_repository = UserRepository(db_session)
    self.auth_service = AuthService(db_session)
    self.db_session = db_session
    
  def get_user_by_id(self, user_id: str) -> User:
    """Retrieve a user by their ID."""
    user = self.user_repository.get_by_id(user_id)
    if not user:
      raise ValueError("User not found")
    return user