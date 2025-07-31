from sqlalchemy.orm import Session
from app.models.user import User

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
