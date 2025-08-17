from sqlalchemy import func
from sqlalchemy.orm import Session, aliased

from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment_schema import CommentCreate, CommentUpdate

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
    comment = self.db.query(Comment).filter(Comment.id == comment_id).first()
    reply_count = (
      self.db.query(func.count(Comment.id))
        .filter(Comment.parent_id == comment_id)
        .scalar()
    )
    return comment, reply_count if comment else None
  
  def get_top_level_comments(self, blog_id: str, limit: int = 10, offset: int = 0):
    """Get top-level comments for a specific blog post."""
    total = (
      self.db.query(func.count(Comment.id))
        .filter(Comment.blog_id == blog_id, Comment.parent_id == None)
        .scalar()
    )

    ChildComment = aliased(Comment)

    # Subquery to count replies for each top-level comment
    subquery = (
      self.db.query(func.count(ChildComment.id))
        .filter(ChildComment.parent_id == Comment.id)
        .correlate(Comment)
        .scalar_subquery()
    )

    comments = (
      self.db.query(Comment, subquery.label("reply_count"))
        .filter(Comment.blog_id == blog_id, Comment.parent_id == None)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return comments, total
  
  def get_all_top_level_comments(self, limit: int = 10, offset: int = 0):
    """Get all comments with pagination."""
    total = (
      self.db.query(func.count(Comment.id))
        .filter(Comment.parent_id == None)
        .scalar()
    )

    ChildComment = aliased(Comment)

    # Subquery to count replies for each top-level comment
    subquery = (
      self.db.query(func.count(ChildComment.id))
        .filter(ChildComment.parent_id == Comment.id)
        .correlate(Comment)
        .scalar_subquery()
    )

    comments = (
      self.db.query(Comment, subquery.label("reply_count"))
        .filter(Comment.parent_id == None)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return comments, total
  
  def get_comment_replies(self, comment_id: str, limit: int = 10, offset: int = 0):
    """Get replies for a specific comment."""
    total = (
      self.db.query(func.count(Comment.id))
        .filter(Comment.parent_id == comment_id)
        .scalar()
    )

    ChildComment = aliased(Comment)
    
    # Subquery to count replies for each reply comment
    subquery = (
      self.db.query(func.count(ChildComment.id))
        .filter(ChildComment.parent_id == Comment.id)
        .correlate(Comment)
        .scalar_subquery()
    )

    replies = (
      self.db.query(Comment, subquery.label("reply_count"))
        .filter(Comment.parent_id == comment_id)
        .order_by(Comment.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return replies, total

  def update(self, comment_id: str, data: CommentUpdate):
    """Update an existing comment."""
    comment, _ = self.get_by_id(comment_id)
    
    for key, value in data.model_dump().items():
      setattr(comment, key, value)
    
    return comment
  
  def delete(self, comment_id: str):
    """Delete a comment by its ID."""
    comment, _ = self.get_by_id(comment_id)
    
    self.db.delete(comment)
  
  def add_user_like(self, comment: Comment, user: User):
    comment.liked_by.append(user)
  
  def remove_user_like(self, comment: Comment, user: User):
    comment.liked_by.remove(user)
    