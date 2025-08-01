from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.models.user import User
from app.services.user_service import UserService
from app.core.config import settings
from app.db.base import SessionDep

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", scheme_name="JWT")

def get_current_user(db_session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
  """Dependency to get the currenet user from the token."""
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"}
  )

  try:
    payload: dict = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    print(f"Decoded payload: {payload}")
    user_id: str = payload.get("user_id")
    
    user_service = UserService(db_session)
    user = user_service.get_user_by_id(user_id)

    return user
    
  except ExpiredSignatureError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Token has expired",
      headers={"WWW-Authenticate": "Bearer"}
    )

  except InvalidTokenError:
    raise credentials_exception

  except ValueError as e:
    raise e
  