from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUserDep
from app.schemas.comment_schema import CommentUpdate, CommentResponse
from app.schemas.shared_schema import PaginatedResponse
from app.services.comment_service import CommentServiceDep 

router = APIRouter(prefix="/comments")

@router.get("/", response_model=PaginatedResponse[CommentResponse])
def get_comments(
  comment_service: CommentServiceDep,
  limit: int = 10,
  offset: int = 0,
):
  """Get a list of comments."""
  try:
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
def get_comment(comment_id: str, comment_service: CommentServiceDep):
  """Get a comment by its ID."""
  try:
    comment = comment_service.get_comment_or_404(comment_id)
    return CommentResponse.model_validate(comment)
  except Exception as e:
    print(f"Error fetching comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.put("/{comment_id}", response_model=CommentResponse, status_code=200)
def update_comment(
  comment_id: str,
  comment_data: CommentUpdate,
  comment_service: CommentServiceDep,
  current_user: CurrentUserDep,
):
  """Update a comment."""
  try:
    comment = comment_service.update_comment(comment_id, comment_data, current_user.id)
    return CommentResponse.model_validate(comment)
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    print(f"Error updating comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/{comment_id}/replies", response_model=PaginatedResponse[CommentResponse], status_code=200)
def get_comment_replies(
  comment_id: str, 
  comment_service: CommentServiceDep, 
  limit: int = 10, 
  offset: int = 0
):
  """Get replies for a specific comment."""
  try:
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

@router.delete("/{comment_id}", status_code=200)
def delete_comment(
  comment_id: str,
  comment_service: CommentServiceDep,
  current_user: CurrentUserDep,
):
  """Delete a comment."""
  try:
    comment_service.delete_comment(comment_id, current_user.id)
    return {"detail": "Comment deleted successfully"}
  except HTTPException as http_exc:
    raise http_exc
  except Exception as e:
    print(f"Error deleting comment: {e}")
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))