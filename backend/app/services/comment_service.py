from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.models.comment import Comment
from app.repositories.comment_repository import CommentRepository
from app.services.blog_service import BlogService
from app.services.user_service import UserService
from app.schemas.comment_schema import CommentCreate

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
  
  def get_comments(self, limit: int = 10, offset: int = 0):
    """Get a paginated list of comments."""
    comments, total = self.comment_repository.get_all_top_level_comments(limit, offset)
    return comments, total

  def get_blog_comments(self, blog_id: str, limit: int = 10, offset: int = 0):
    """Get comments for a specific blog post."""
    return self.comment_repository.get_top_level_comments(blog_id, limit, offset)

  def get_comment_or_404(self, comment_id: str):
    """Get a comment by its ID."""
    comment, reply_count = self.comment_repository.get_by_id(comment_id)
    if not comment:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Comment not found")
    return comment, reply_count

  def _validate_comment_data(self, data: CommentCreate) -> None:
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
      parent_comment, _ = self.get_comment_or_404(parent_id)

      if str(parent_comment.blog_id) != blog_id:
        raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST,
          detail="Parent comment does not belong to the specified blog"
        )
  
  def _process_comment_data(self, data: CommentCreate) -> CommentCreate:
    """Process and convert comment data to the appropriate types."""
    data.author_id = UUID(data.author_id) if isinstance(data.author_id, str) else data.author_id
    data.blog_id = UUID(data.blog_id) if isinstance(data.blog_id, str) else data.blog_id
    data.parent_id = UUID(data.parent_id) if (isinstance(data.parent_id, str) and data.parent_id) else None

    return data