from fastapi import HTTPException, status, Depends, requests
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import CurrentUserDep 
from app.schemas.auth_schema import TokenResponse, ChangePasswordRequest
from app.schemas.user_schema import UserCreate, UserResponse
from app.services.auth_service import AuthServiceDep 

router = APIRouter(
  prefix="/auth",
)

@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, auth_service: AuthServiceDep):
  """Register a new user."""
  try: 
    created_user = auth_service.create_user(user)
    return UserResponse.model_validate(created_user)

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse, status_code=200)
def login_user(
  auth_service: AuthServiceDep,
  form_data: OAuth2PasswordRequestForm = Depends()
):
  """Login a user and return access and refresh tokens."""
  try:
    response = auth_service.authenticate_user(form_data)
    
    return response

  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except Exception as e:
    print(f"Error during login: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/logout", status_code=204)
def logout_user(
  auth_service: AuthServiceDep,
  user: CurrentUserDep
):
  try:
    auth_service.logout_user(user)
    return {"detail": "Successfully logged out"}
  except Exception as e:
    print(f"Error during logout: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/refresh", response_model=TokenResponse, status_code=200)
def refresh_token(
  auth_service: AuthServiceDep,
  req: requests.Request,
  user: CurrentUserDep
):
  """Refresh the access token using the refresh token."""
  try:
    response = auth_service.refresh_user_token(user, req)
    return response
  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except Exception as e:
    print(f"Error during token refresh: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/change-password", status_code=200)
def change_password(
  password_data: ChangePasswordRequest,
  auth_service: AuthServiceDep,
  user: CurrentUserDep
):
  """Change the password of the current user."""
  try:
    user = auth_service.change_user_password(user, password_data.current_password, password_data.new_password)
    
    return {"detail": "Password changed successfully"}
  except Exception as e:
    print(f"Error changing password: {str(e)}")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))