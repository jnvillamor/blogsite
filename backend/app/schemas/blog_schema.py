from __future__ import annotations
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class BlogBase(BaseModel):
  title: str
  content: str

class BlogCreate(BlogBase):
  author_id: str

class BlogUpdate(BlogCreate):
  pass

class BlogSimple(BlogBase):
  id: UUID
  created_at: datetime
  updated_at: datetime

  model_config = {
    "from_attributes": True,
  }

class BlogResponse(BlogBase):
  id: UUID
  author_id: UUID 
  created_at: datetime
  updated_at: datetime

  author: "UserSimple"

  model_config = {
    "from_attributes": True,
  }

from app.schemas.user_schema import UserSimple
BlogResponse.model_rebuild()