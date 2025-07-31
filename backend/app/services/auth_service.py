from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
import jwt

from app.schemas.user_schema import UserCreate
from app.models.user import User
from app.repositories.user_respository import UserRepository
from app.core.config import settings

class AuthService:
  def __init__(self, db_session: Session):
    self.db_session = db_session
    self.user_repository = UserRepository(db_session)
    self.secret_key = settings.SECRET_KEY
    self.jwt_algorithm = settings.JWT_ALGORITHM
    self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
     
  def create_user(self, user_create: UserCreate) -> User:
    """Create a new user in the database."""
    try:
      # Check if the user email already exists
      existing_user = self.user_repository.get_by_email(user_create.email)

      if existing_user:
        raise ValueError("Email already registered")
      
      # Encrypt the password before saving
      user_data = user_create.model_dump(exclude={"password"})
      user_data['hashed_password'] = self._encrypt_password(user_create.password)

      # Create a new user instance
      user = self.user_repository.create(user_data)

      # Return the created user
      return user
    
    except Exception as e:
      raise e
    
  def authenticate_user(self, credentials: OAuth2PasswordRequestForm) -> dict:
    """Authenticate a user and return tokens."""
    try:
      user = self.user_repository.get_by_email(credentials.username)

      if not user or not self._verify_password(credentials.password, user.hashed_password):
        raise ValueError("Invalid email or password")
      
      access_token = self._create_tokens(user, type='access')
      refresh_token = self._create_tokens(user, type='refresh')

      return {
        "user_id": user.id,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
      }
    
    except Exception as e:
      raise e

  def _create_tokens(self, user: User, type: Literal['access', 'refresh']) -> str:
    """Create JWT token for the user."""
    expiration = timedelta(hours=1) if type == 'access' else timedelta(days=7)
    token_data = {
      "user_id": str(user.id),
      "exp": datetime.now(timezone.utc) + expiration,
      "type": type
    }
    token = jwt.encode(token_data, self.secret_key, algorithm=self.jwt_algorithm)
    return token
  
  def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
    """Verify the provided password against the stored hashed password."""
    return self.pwd_context.verify(plain_password, hashed_password)

  def _encrypt_password(self, password: str) -> str:
    """Encrypt the password using a hashing algorithm."""
    return self.pwd_context.hash(password)