from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter
from app.schemas.user_schema import  UserResponse
from app.db.base import SessionDep
from app.api.dependencies import get_current_user
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(
  prefix="/users",
)

@router.post("/me", response_model=UserResponse, status_code=201)
async def current_user(user: User = Depends(get_current_user)):
  """Get the current user."""
  try:
    return UserResponse.model_validate(user)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
