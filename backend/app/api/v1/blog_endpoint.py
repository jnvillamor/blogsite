from fastapi import HTTPException, status, Depends
from fastapi.routing import APIRouter

from app.api.dependencies import get_current_user
from app.db.base import SessionDep
from app.models.user import User
from app.services.blog_service import BlogService
from app.schemas.blog_schema import BlogCreate, BlogResponse
from app.schemas.shared_schema import PaginatedResponse

router = APIRouter(
  prefix="/blogs",
)

@router.post("/", response_model=BlogResponse, status_code=201)
def create_blog(
  blog_data: BlogCreate,
  db_session: SessionDep,
  current_user: User = Depends(get_current_user),
):
  """Create a new blog post."""
  try:
    blog_service = BlogService(db_session)
    blog = blog_service.create_blog(blog_data, current_user.id)
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=PaginatedResponse[BlogResponse])
def get_blogs(
  session: SessionDep,
  limit: int = 5,
  offset: int = 0,
):
  """Get all blogs"""
  try:
    blog_service = BlogService(session)
    blogs, total = blog_service.get_blogs(limit, offset)

    return PaginatedResponse[BlogResponse](
      items=blogs,
      total=total,
      limit=limit,
      offset=offset
    )
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/{blog_id}", response_model=BlogResponse, status_code=200)
def get_blog_by_id(blog_id: str, session: SessionDep):
  """Get a blog by its ID."""
  try:
    blog_service = BlogService(session)
    blog = blog_service.get_blog_by_id(blog_id)
    
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
      