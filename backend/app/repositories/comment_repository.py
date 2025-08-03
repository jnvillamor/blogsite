from sqlalchemy.orm import Session

from app.models.comment import Comment
from app.schemas.comment_schema import CommentCreate

class CommentRepository:
  def __init__(self, db: Session):
    self.db = db
  
  def create(self, comment_data: CommentCreate):
    """Create a new comment."""
    comment = Comment(**comment_data.model_dump())
    self.db.add(comment)
    return comment
    
  def get_by_id(self, comment_id: str):
    """Retrieve a comment by its ID."""
    return self.db.query(Comment).filter(Comment.id == comment_id).first()