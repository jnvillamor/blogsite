from fastapi import HTTPException, status, Depends, requests
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import TokenResponse
from app.db.base import SessionDep
from app.services.auth_service import AuthService
from app.models.user import User
from app.api.dependencies import get_current_user

router = APIRouter(
  prefix="/auth",
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, session: SessionDep):
  """Register a new user."""
  try: 

    auth_service = AuthService(session)
    created_user = auth_service.create_user(user)
    return UserResponse.model_validate(created_user)

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse, status_code=200)
def login_user(
  session: SessionDep,
  req: requests.Request,
  form_data: OAuth2PasswordRequestForm = Depends()
):
  """Login a user and return access and refresh tokens."""
  try:
    auth_service = AuthService(session)
    response = auth_service.authenticate_user(form_data, req)
    
    return response

  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except Exception as e:
    print(f"Error during login: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/refresh", response_model=TokenResponse, status_code=200)
def refresh_token(
  session: SessionDep,
  req: requests.Request,
  user: User = Depends(get_current_user)
):
  """Refresh the access token using the refresh token."""
  try:
    auth_service = AuthService(session)
    response = auth_service.refresh_user_token(user, req)
    return response
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except Exception as e:
    print(f"Error during token refresh: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))