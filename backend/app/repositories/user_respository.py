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
    new_user = User(**user)
    self.db_session.add(new_user)
    self.db_session.commit()
    self.db_session.refresh(new_user)

    return new_user
    
    
  def change_password(self, user: User, new_password: str) -> User:
    """Change the user's password."""
    user.hashed_password = new_password
    self.db_session.commit()
    self.db_session.refresh(user)
    return user
  
  def update_info(self, user: User, user_data: UserUpdate) -> User:
    """Update user information."""
    for key, value in user_data.dict(exclude_unset=True).items():
      setattr(user, key, value)
    
    self.db_session.commit()
    self.db_session.refresh(user)
    return user