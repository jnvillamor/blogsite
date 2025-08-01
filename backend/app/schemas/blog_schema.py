from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

from .user_schema import UserSimple

class BlogBase(BaseModel):
  title: str
  content: str

class BlogCreate(BlogBase):
  author_id: str

class BlogSimple(BlogBase):
  id: UUID
  created_at: datetime
  updated_at: datetime

class BlogResponse(BlogBase):
  id: UUID
  author_id: UUID 
  created_at: datetime
  updated_at: datetime

  author: UserSimple

  model_config = {
    "from_attributes": True,
  }