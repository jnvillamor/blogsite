from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user_schema import UserCreate, UserResponse
from app.schemas.auth_schema import TokenResponse
from app.db.base import SessionDep
from app.services.auth_service import AuthService

router = APIRouter(
  prefix="/auth",
)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, session: SessionDep):
  """Register a new user."""
  try: 

    auth_service = AuthService(session)
    created_user = auth_service.create_user(user)
    return UserResponse.model_validate(created_user)

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=TokenResponse, status_code=200)
async def login_user(
  session: SessionDep,
  form_data: OAuth2PasswordRequestForm = Depends()
):
  """Login a user and return access and refresh tokens."""
  try:
    auth_service = AuthService(session)
    tokens = auth_service.authenticate_user(form_data)
    return TokenResponse.model_validate(tokens)

  except ValueError as e:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
  