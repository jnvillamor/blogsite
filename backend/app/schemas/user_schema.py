from pydantic import BaseModel
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
  email: str 
  first_name: str
  last_name: str

class UserCreate(UserBase):
  password: str

class UserResponse(UserBase):
  id: UUID
  created_at: datetime
  updated_at: datetime

  model_config = {
    "from_attributes": True,
  }