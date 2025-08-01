from passlib.context import CryptContext
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime, timezone
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import requests, responses
import jwt

from app.schemas.user_schema import UserCreate
from app.schemas.auth_schema import TokenResponse
from app.models.user import User
from app.repositories.user_respository import UserRepository
from app.core.config import settings
from app.services.redis_service import RedisService

class AuthService:
  def __init__(self, db_session: Session):
    self.db_session = db_session
    self.user_repository = UserRepository(db_session)
    self.redis_service = RedisService()
    self.secret_key = settings.SECRET_KEY
    self.jwt_algorithm = settings.JWT_ALGORITHM
    self.jwt_access_token_ex = settings.JWT_ACCESS_TOKEN_EX
    self.jwt_refresh_token_ex = settings.JWT_REFRESH_TOKEN_EX
    self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
     
  def create_user(self, user_create: UserCreate) -> User:
    """Create a new user in the database."""
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
    
  def authenticate_user(self, credentials: OAuth2PasswordRequestForm) -> responses.JSONResponse:
    """Authenticate a user and return tokens."""
    user = self.user_repository.get_by_email(credentials.username)

    if not user or not self._verify_password(credentials.password, user.hashed_password):
      raise ValueError("Invalid email or password")
    
    access_token = self._create_tokens(user, type='access')
    refresh_token = self._create_tokens(user, type='refresh')

    # Store refresh token in Redis with an expiration time
    self.redis_service.set(f"refresh_token:{user.id}", refresh_token, ex=self.jwt_refresh_token_ex)

    response = responses.JSONResponse(content=TokenResponse(
      user_id=str(user.id),
      access_token=access_token,
      refresh_token=refresh_token,
      token_type="bearer"
    ).model_dump())

    # Set the cookie for the refresh token
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,
    )

    return response
    
  def refresh_user_token(self, user: User, req: requests.Request) -> responses.JSONResponse:
    """Refresh the access token using the refresh token."""
    # Verify the refresh token from Redis
    refresh_token = req.cookies.get("refresh_token")
    
    if not refresh_token or not self.redis_service.exists(f"refresh_token:{user.id}"):
      raise ValueError("Invalid or expired refresh token")
    
    if not self.redis_service.get(f"refresh_token:{user.id}") == refresh_token:
      raise ValueError("Refresh token mismatch")
    
    # Create a new access token
    access_token = self._create_tokens(user, type='access')
    refresh_token = self._create_tokens(user, type='refresh')
    
    # Update the refresh token in Redis
    self.redis_service.set(f"refresh_token:{user.id}", refresh_token, ex=self.jwt_refresh_token_ex)
    
    response = responses.JSONResponse(content=TokenResponse(
      user_id=str(user.id),
      access_token=access_token,
      refresh_token=refresh_token,
      token_type="bearer"
    ).model_dump())
    
    # Set the cookie for the new refresh token
    response.set_cookie(
      key="refresh_token",
      value=refresh_token,
      httponly=True,
    )
    
    return response
    
  def logout_user(self, user: User) -> bool:
    """Logout the user by deleting the refresh token from Redis."""
    # Delete the refresh token from Redis
    self.redis_service.delete(f"refresh_token:{user.id}")
    return True
  
  def change_user_password(self, user: User, current_password: str, new_password: str) -> User:
    """Change the user's password."""
    if not self._verify_password(current_password, user.hashed_password):
      raise ValueError("Current password is incorrect")
    
    # Encrypt the new password
    encrypted_password = self._encrypt_password(new_password)
    user = self.user_repository.change_password(user, encrypted_password)

    return user

  def _create_tokens(self, user: User, type: Literal['access', 'refresh']) -> str:
    """Create JWT token for the user."""
    expiration = self.jwt_access_token_ex if type == 'access' else self.jwt_refresh_token_ex
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