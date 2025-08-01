from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserUpdate

class UserRepository:
  def __init__(self, db_session: Session):
    self.db_session = db_session
  
  def get_by_email(self, email: str) -> User | None:
    """Retrieve a user by email."""
    return self.db_session.query(User).filter_by(email=email).first()
  
  def get_by_id(self, user_id: str) -> User | None:
    """Retrieve a user by ID."""
    return self.db_session.query(User).filter_by(id=user_id).first()

  def create(self, user: dict) -> User:
    """Create a new user in the database."""
    try:
      new_user = User(**user)
      self.db_session.add(new_user)
      self.db_session.commit()
      self.db_session.refresh(new_user)

      return new_user
    
    except Exception as e:
      self.db_session.rollback()
      raise e
    
  def change_password(self, user: User, new_password: str) -> User:
    """Change the user's password."""
    try:
      user.hashed_password = new_password
      self.db_session.commit()
      self.db_session.refresh(user)
      return user
    except Exception as e:
      self.db_session.rollback()
      raise e
  
  def update_info(self, user: User, user_data: UserUpdate) -> User:
    """Update user information."""
    try:
      user.email = user_data.email or user.email
      user.first_name = user_data.first_name or user.first_name
      user.last_name = user_data.last_name or user.last_name
      
      self.db_session.commit()
      self.db_session.refresh(user)
      return user
    except Exception as e:
      self.db_session.rollback()
      raise e