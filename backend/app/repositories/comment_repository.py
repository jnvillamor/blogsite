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
  
  def get_top_level_comments(self, blog_id: str, limit: int = 10, offset: int = 0):
    """Get top-level comments for a specific blog post."""
    query = ( 
      self.db.query(Comment)
        .filter(Comment.blog_id == blog_id, Comment.parent_id == None)
        .order_by(Comment.created_at.desc())
    )
    total = query.count()
    comments = query.offset(offset).limit(limit).all()
    return comments, total