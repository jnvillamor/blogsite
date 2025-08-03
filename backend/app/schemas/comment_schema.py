from datetime import datetime
from pydantic import BaseModel
from uuid import UUID

class CommentBase(BaseModel):
  content: str
  author_id: UUID | str
  blog_id: UUID | str
  parent_id: UUID | str | None = None

class CommentCreate(CommentBase):
  pass

class CommentResponse(CommentBase):
  id: UUID
  created_at: datetime
  updated_at: datetime
  replies: list["CommentResponse"] = []

  model_config = {
    "from_attributes": True,
  }

CommentResponse.model_rebuild()