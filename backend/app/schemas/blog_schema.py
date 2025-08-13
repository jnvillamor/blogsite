from __future__ import annotations
from datetime import datetime
from pydantic import BaseModel
from typing import List 
from uuid import UUID

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
  liked_by: List["UserSimple"] = []

  model_config = {
    "from_attributes": True,
  }

from app.schemas.user_schema import UserSimple
BlogResponse.model_rebuild()