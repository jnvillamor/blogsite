from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.services.auth_service import AuthService
from sqlalchemy.orm import Session

class UserService:
  def __init__(self, db_session: Session):
    self.auth_service = AuthService()
    self.db_session = db_session
    
  def create_user(self, user_create: UserCreate) -> User:
    """Create a new user in the database."""
    try:
      # Check if the user email already exists 
      existing_user = self.db_session.query(User).filter_by(email=user_create.email).first()

      if existing_user:
        raise ValueError("Email already registered")
      
      # Encrypt the password before saving
      user_data = user_create.model_dump(exclude={"password"})
      user_data['hashed_password'] = self.auth_service.encrypt_password(user_create.password)
      
      # Create a new user instance
      user = User(**user_data)
      self.db_session.add(user)
      self.db_session.commit()
      self.db_session.refresh(user)

      # Return the created user
      return user
    
    except Exception as e:
      self.db_session.rollback()
      raise e