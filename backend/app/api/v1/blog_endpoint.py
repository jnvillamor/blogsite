from fastapi import HTTPException, status, Request 
from fastapi.routing import APIRouter

from app.api.dependencies import CurrentUserDep
from app.core.limiter import limiter
from app.services.blog_service import BlogServiceDep
from app.services.comment_service import CommentServiceDep 
from app.schemas.blog_schema import BlogCreate, BlogResponse, BlogUpdate
from app.schemas.comment_schema import CommentCreate, CommentResponse
from app.schemas.shared_schema import PaginatedResponse

router = APIRouter(
  prefix="/blogs",
)

@router.post("/", response_model=BlogResponse, status_code=201)
@limiter.limit("100/hour")
def create_blog(
  request: Request,
  blog_data: BlogCreate,
  blog_service: BlogServiceDep,
  current_user: CurrentUserDep,
):
  """Create a new blog post."""
  try:
    blog = blog_service.create_blog(blog_data, str(current_user.id))
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/", response_model=PaginatedResponse[BlogResponse])
@limiter.limit("1000/hour")
def get_blogs(
  request: Request,
  blog_service: BlogServiceDep,
  limit: int = 5,
  offset: int = 0,
):
  """Get all blogs"""
  try:
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
@limiter.limit("1000/hour")
def get_blog_by_id(
  blog_id: str, 
  request: Request,
  blog_service: BlogServiceDep
):
  """Get a blog by its ID."""
  try:
    blog = blog_service.get_blog_or_404(blog_id)
    
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
      
@router.put("/{blog_id}", response_model=BlogResponse, status_code=200)
@limiter.limit("1000/hour")
def update_blog(
  blog_id: str,
  request: Request,
  blog_data: BlogUpdate,
  blog_service: BlogServiceDep,
  current_user: CurrentUserDep,
):
  """Update a blog post."""
  try:
    blog = blog_service.update_blog(blog_id, blog_data, str(current_user.id))
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.delete("/{blog_id}", status_code=200)
@limiter.limit("1000/hour")
def delete_blog(
  blog_id: str,
  request: Request,
  blog_service: BlogServiceDep,
  current_user: CurrentUserDep,
):
  """Delete a blog post."""
  try:
    blog_service.delete_blog(blog_id, str(current_user.id))
    return {"detail": "Blog deleted successfully"}
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{blog_id}/comments", response_model=CommentResponse, status_code=201)
@limiter.limit("1000/hour")
def create_comment(
  blog_id: str,
  request: Request,
  comment_data: CommentCreate,
  comment_service: CommentServiceDep,
  current_user: CurrentUserDep,
):
  """Create a new comment on a blog post."""
  try:
    comment = comment_service.create_comment(data=comment_data)

    return CommentResponse.model_validate(comment)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/{blog_id}/comments", response_model=PaginatedResponse[CommentResponse], status_code=200)
@limiter.limit("1000/hour")
def get_comments(
  blog_id: str,
  request: Request,
  comment_service: CommentServiceDep,
  limit: int = 5,
  offset: int = 0,
):
  """Get all comments for a blog post."""
  try:
    comments, total = comment_service.get_blog_comments(blog_id, limit, offset)
    
    return PaginatedResponse[CommentResponse](
      items=comments,
      total=total,
      limit=limit,
      offset=offset
    )
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.put("/{blog_id}/toggle-like", response_model=BlogResponse, status_code=200)
@limiter.limit("1000/hour")
def toggle_like_blog(
  blog_id: str,
  request: Request,
  blog_service: BlogServiceDep,
  current_user: CurrentUserDep
):
  """Toggle like status for a blog post."""
  try:
    blog = blog_service.toggle_blog_like(blog_id, current_user)
    return BlogResponse.model_validate(blog)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))