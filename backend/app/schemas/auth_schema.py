from pydantic import BaseModel

class TokenResponse(BaseModel):
  """Schema for token response."""
  user_id: str
  access_token: str
  refresh_token: str
  token_type: str = "bearer"

class ChangePasswordRequest(BaseModel):
  """Schema for change password request."""
  current_password: str
  new_password: str