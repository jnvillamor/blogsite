from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from uuid import UUID

from app.db.base import SessionDep
from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.services.blog_service import BlogService
from app.services.user_service import UserService
from app.schemas.comment_schema import CommentCreate, CommentUpdate

class CommentService:
  def __init__(self, db_session: Session):
    self.db_session = db_session
    self.comment_repository = CommentRepository(db_session)
    self.blog_service = BlogService(db_session)
    self.user_service = UserService(db_session)
  
  def create_comment(
    self,
    data: CommentCreate,
  ) -> Comment:
    """Create a new comment on a blog post."""
    try:
      # Validate the comment data
      self._validate_comment_data(data)

      # Validate references
      self._validate_comment_reference(data.blog_id, data.author_id, data.parent_id)

      # Process the comment data
      data = self._process_comment_data(data)

      # Create the comment
      comment = self.comment_repository.create(data)
      self.db_session.commit()
      self.db_session.refresh(comment)
      
      return comment
    except HTTPException as http_exc:
      self.db_session.rollback()
      raise http_exc
    except Exception as e:
      print(f"Error creating comment: {e}")
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  def get_comments(self, limit: int = 10, offset: int = 0) -> tuple:
    """Get a paginated list of comments."""
    comments, total = self.comment_repository.get_all_top_level_comments(limit, offset)
    items = [] 
    for comment, reply_count in comments:
      comment.__dict__['reply_count'] = reply_count
      items.append(comment)

    return items, total

  def get_blog_comments(self, blog_id: str, limit: int = 10, offset: int = 0) -> tuple:
    """Get comments for a specific blog post."""
    comments, total = self.comment_repository.get_top_level_comments(blog_id, limit, offset)
    items = []
    for comment, reply_count in comments:
      comment.__dict__['reply_count'] = reply_count
      items.append(comment)

    return items, total

  def get_comment_or_404(self, comment_id: str) -> Comment:
    """Get a comment by its ID."""
    comment, reply_count = self.comment_repository.get_by_id(comment_id)

    if not comment:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    
    comment.__dict__['reply_count'] = reply_count
    
    return comment
  
  def get_comment_replies(self, comment_id: str, limit: int = 10, offset: int = 0) -> tuple:
    """Get replies for a specific comment."""
    comment = self.get_comment_or_404(comment_id)
    replies, total = self.comment_repository.get_comment_replies(
      comment_id=comment.id,
      limit=limit,
      offset=offset
    )
    
    items = [] 
    for reply, reply_count in replies:
      reply.__dict__['reply_count'] = reply_count
      items.append(reply)

    return items, total

  def update_comment(
    self,
    comment_id: str,
    data: CommentUpdate,
    author_id: str,
  ) -> Comment:
    """Update an existing comment."""
    try:
      # Validate the comment data
      self._validate_comment_data(data)
      
      # Validate references
      self._validate_comment_reference(data.blog_id, author_id, data.parent_id)
      
      comment = self.get_comment_or_404(comment_id)
      if str(comment.author_id) != author_id:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="You do not have permission to update this comment"
        )
      
      # Process the comment data
      data = self._process_comment_data(data)
      
      # Update the comment
      updated_comment = self.comment_repository.update(comment_id, data)
      self.db_session.commit()
      self.db_session.refresh(updated_comment)

      return updated_comment

    except HTTPException as http_exc:
      raise http_exc
    except Exception as e:
      print(f"Error updating comment: {e}")
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
  
  def delete_comment(self, comment_id: str, author_id: str) -> None:
    """Delete a comment."""
    try:
      comment = self.get_comment_or_404(comment_id)
      if str(comment.get("author_id")) != author_id:
        raise HTTPException(
          status_code=status.HTTP_403_FORBIDDEN,
          detail="You do not have permission to delete this comment"
        )
      self.comment_repository.delete(comment_id)
      self.db_session.commit()

    except HTTPException as http_exc:
      self.db_session.rollback()
      raise http_exc
    except Exception as e:
      print(f"Error deleting comment: {e}")
      self.db_session.rollback()
      raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

  def _validate_comment_data(self, data: CommentCreate | CommentUpdate) -> None:
    """Validate the comment data."""
    for key, value in data.model_dump().items():
      if value is None:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail=f"{key} is required"
        )

  def _validate_comment_reference(self, blog_id: str, author_id: str, parent_id: str = None) -> None:
    """Validate the blog and author references for the comment."""
    blog = self.blog_service.get_blog_or_404(blog_id)
    user = self.user_service.get_user_or_404(author_id)

    parent_comment = None
    if parent_id:
      parent_comment = self.get_comment_or_404(parent_id)

      if str(parent_comment.blog_id) != blog_id:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Parent comment does not belong to the specified blog"
        )
  
  def _process_comment_data(self, data: CommentCreate | CommentUpdate) -> CommentCreate | CommentUpdate:
    """Process and convert comment data to the appropriate types."""
    data.author_id = UUID(data.author_id) if isinstance(data.author_id, str) else data.author_id
    data.blog_id = UUID(data.blog_id) if isinstance(data.blog_id, str) else data.blog_id
    data.parent_id = UUID(data.parent_id) if (isinstance(data.parent_id, str) and data.parent_id) else None

    return data

def get_comment_service(db_session: SessionDep) -> CommentService:
    """Get the comment service instance."""
    return CommentService(db_session)
  
CommentServiceDep = Annotated[CommentService, Depends(get_comment_service)]