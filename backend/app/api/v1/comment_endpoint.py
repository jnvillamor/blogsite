from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.base import SessionDep
from app.models.user import User
from app.api.dependencies import get_current_user
from app.schemas.comment_schema import CommentUpdate, CommentResponse
from app.schemas.shared_schema import PaginatedResponse
from app.services.comment_service import CommentService

router = APIRouter(prefix="/comments")

@router.get("/", response_model=PaginatedResponse[CommentResponse])
def get_comments(
  db: SessionDep,
  limit: int = 10,
  offset: int = 0,
):
  """Get a list of comments."""
  try:
    comment_service = CommentService(db)
    comments, total = comment_service.get_comments(limit=limit, offset=offset)
    
    return PaginatedResponse[CommentResponse](
      items=comments,
      total=total,
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    print(f"Error fetching comments: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{comment_id}", response_model=CommentResponse, status_code=200)
def get_comment(comment_id: str, db: SessionDep):
  """Get a comment by its ID."""
  try:
    comment_service = CommentService(db)
    comment = comment_service.get_comment_or_404(comment_id)
    return CommentResponse.model_validate(comment)
  except Exception as e:
    print(f"Error fetching comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{comment_id}", response_model=CommentResponse, status_code=200)
def update_comment(
  comment_id: str,
  comment_data: CommentUpdate,
  db: SessionDep,
  current_user: User = Depends(get_current_user),
):
  """Update a comment."""
  try:
    comment_service = CommentService(db)
    comment = comment_service.update_comment(comment_id, comment_data, current_user.id)
    return CommentResponse.model_validate(comment)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    print(f"Error updating comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{comment_id}/replies", response_model=PaginatedResponse[CommentResponse], status_code=200)
def get_comment_replies(comment_id: str, db: SessionDep, limit: int = 10, offset: int = 0):
  """Get replies for a specific comment."""
  try:
    comment_service = CommentService(db)
    replies, total = comment_service.get_comment_replies(comment_id, limit=limit, offset=offset)

    return PaginatedResponse[CommentResponse](
      items=replies,
      total=total,
      limit=limit,
      offset=offset,
    )
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))