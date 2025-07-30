from passlib.context import CryptContext

class AuthService:
  def __init__(self):
    self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
  
  def encrypt_password(self, password: str) -> str:
    """Encrypt the password using a hashing algorithm."""
    return self.pwd_context.hash(password)