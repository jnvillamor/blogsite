from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta

class Settings(BaseSettings):
  APP_NAME: str = "Blogsite API"
  DATABASE_URL: str = "sqlite:///./test.db"
  SECRET_KEY: str
  JWT_ALGORITHM: str = "HS256"
  JWT_ACCESS_TOKEN_EX: timedelta = timedelta(minutes=15)
  JWT_REFRESH_TOKEN_EX: timedelta = timedelta(days=7)

  model_config = SettingsConfigDict(
    env_file=".env",
  )

settings = Settings()