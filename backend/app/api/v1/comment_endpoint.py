from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from app.db.base import SessionDep
from app.models.comment import Comment
from app.schemas.comment_schema import CommentCreate, CommentResponse
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
      items=[
          CommentResponse.model_validate({
          **comment.__dict__,
          "reply_count": reply_count
         }) for comment, reply_count in comments
      ],
      total=total,
      limit=limit,
      offset=offset,
    )
  except Exception as e:
    print(f"Error fetching comments: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{comment_id}", response_model=CommentResponse)
def get_comment(comment_id: str, db: SessionDep):
  """Get a comment by its ID."""
  try:
    comment_service = CommentService(db)
    comment, reply_count = comment_service.get_comment_or_404(comment_id)
    return CommentResponse.model_validate({
      **comment.__dict__,
      "reply_count": reply_count
    })
  except Exception as e:
    print(f"Error fetching comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))