from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter
from app.db.base import SessionDep
from app.api.dependencies import get_current_user
from app.schemas.blog_schema import BlogResponse
from app.schemas.shared_schema import PaginatedResponse
from app.schemas.user_schema import  UserResponse, UserUpdate, UserSimple
from app.services.user_service import UserService
from app.models.user import User

router = APIRouter(
  prefix="/users",
)

@router.post("/me", response_model=UserSimple, status_code=201)
def current_user(user: User = Depends(get_current_user)):
  """Get the current user."""
  try:
    return UserSimple.model_validate(user)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user_by_id(user_id: str, db_session: SessionDep):
  """Get user by ID."""
  try:
    user_service = UserService(db_session)
    user = user_service.get_user_or_404(user_id, with_blogs=True)
    
    return UserResponse.model_validate(user)
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{user_id}/blogs", response_model=PaginatedResponse[BlogResponse], status_code=200)
def get_user_blogs(
  user_id: str,
  db_session: SessionDep,
  limit: int = 5,
  offset: int = 0
):
  """Get all blogs by a specific user."""
  try:
    user_service = UserService(db_session)
    blogs, total = user_service.get_user_blogs(user_id, limit, offset)
    
    return PaginatedResponse[BlogResponse](
      items=[BlogResponse.model_validate(blog) for blog in blogs],
      total=total,
      limit=limit,
      offset=offset
    )
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{user_id}/update", response_model=UserResponse, status_code=200)
def update_user(
  db_session: SessionDep,
  user_data: UserUpdate,
  user_id: str,
  current_user: User = Depends(get_current_user),
):
  """Update user information."""
  try:
    user_service = UserService(db_session)
    updated_user = user_service.update_user(current_user, user_id, user_data)
    return UserResponse.model_validate(updated_user)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
