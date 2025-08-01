from pydantic import BaseModel

class TokenResponse(BaseModel):
  """Schema for token response."""
  user_id: str
  access_token: str
  refresh_token: str
  token_type: str = "bearer"