from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  APP_NAME: str = "Blogsite API"
  DATABASE_URL: str = "sqlite:///./test.db"

  model_config = SettingsConfigDict(
    env_file=".env",
  )