from fastapi import HTTPException, status
from fastapi.routing import APIRouter
from app.schemas.user_schema import UserCreate, UserResponse
from app.db.session import SessionDep
from app.services.user_service import UserService

router = APIRouter(
  prefix="/auth",
)

@router.post("/register", response_model=UserResponse, status_code=201)
async def register_user(user: UserCreate, session: SessionDep):
  """Register a new user."""
  try: 

    user_service = UserService(session)
    created_user = user_service.create_user(user)
    return UserResponse.model_validate(created_user)

  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))