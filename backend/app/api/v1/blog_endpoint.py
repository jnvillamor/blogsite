from fastapi import HTTPException, status, Depends, responses
from fastapi.routing import APIRouter

from app.api.dependencies import get_current_user
from app.db.base import SessionDep
from app.models.user import User
from app.services.blog_service import BlogService
from app.services.comment_service import CommentService
from app.schemas.blog_schema import BlogCreate, BlogResponse, BlogUpdate
from app.schemas.comment_schema import CommentCreate, CommentResponse
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
    blog = blog_service.get_blog_or_404(blog_id)
    
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
      
@router.put("/{blog_id}", response_model=BlogResponse, status_code=200)
def update_blog(
  blog_id: str,
  blog_data: BlogUpdate,
  session: SessionDep,
  current_user: User = Depends(get_current_user),
):
  """Update a blog post."""
  try:
    blog_service = BlogService(session)
    blog = blog_service.update_blog(blog_id, blog_data, current_user.id)
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{blog_id}", status_code=200)
def delete_blog(
  blog_id: str,
  session: SessionDep,
  current_user: User = Depends(get_current_user),
):
  """Delete a blog post."""
  try:
    blog_service = BlogService(session)
    blog_service.delete_blog(blog_id, current_user.id)
    return {"detail": "Blog deleted successfully"}
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{blog_id}/comments", response_model=CommentResponse, status_code=201)
def create_comment(
  blog_id: str,
  comment_data: CommentCreate,
  session: SessionDep,
  current_user: User = Depends(get_current_user),
):
  """Create a new comment on a blog post."""
  try:
    comment_service = CommentService(session)
    comment = comment_service.create_comment(data=comment_data)

    return CommentResponse.model_validate(comment)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{blog_id}/comments", response_model=PaginatedResponse[CommentResponse], status_code=200)
def get_comments(
  blog_id: str,
  session: SessionDep,
  limit: int = 5,
  offset: int = 0,
):
  """Get all comments for a blog post."""
  try:
    comment_service = CommentService(session)
    comments, total = comment_service.get_blog_comments(blog_id, limit, offset)
    
    return PaginatedResponse[CommentResponse](
      items=[
        CommentResponse.model_validate({
          **comment.__dict__,
          "reply_count": reply_count
          }) for comment, reply_count in comments
      ],
      total=total,
      limit=limit,
      offset=offset
    )
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))