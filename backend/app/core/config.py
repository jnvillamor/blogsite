from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  APP_NAME: str = "Blogsite API"
  DATABASE_URL: str = "sqlite:///./test.db"
  SECRET_KEY: str
  JWT_ALGORITHM: str = "HS256"

  model_config = SettingsConfigDict(
    env_file=".env",
  )

settings = Settings()