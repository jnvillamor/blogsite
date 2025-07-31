from pydantic import BaseModel
from uuid import UUID

class TokenResponse(BaseModel):
  """Schema for token response."""
  user_id: UUID
  access_token: str
  refresh_token: str
  token_type: str = "bearer"