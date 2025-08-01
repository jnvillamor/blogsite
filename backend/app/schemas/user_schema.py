from datetime import datetime
from pydantic import BaseModel
from typing import List
from uuid import UUID

class UserBase(BaseModel):
  email: str 
  first_name: str
  last_name: str

class UserSimple(UserBase):
  id: UUID
  created_at: datetime
  updated_at: datetime

  model_config = {
    "from_attributes": True,
  }

class UserCreate(UserBase):
  password: str

class UserUpdate(UserBase):
  pass

class UserResponse(UserBase):
  id: UUID
  created_at: datetime
  updated_at: datetime

  blogs: List["BlogSimple"] = []

  model_config = {
    "from_attributes": True,
  }

from app.schemas.blog_schema import BlogSimple
UserResponse.model_rebuild()