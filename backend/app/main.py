from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.api.v1 import register_routes
from app.core.limiter import limiter

def create_app() -> FastAPI:
  app = FastAPI(title="Blogsite API")
  app.state.limiter = limiter
  app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

  @app.get("/")
  def root():
    return {"message": "Welcome to the Blogsite API"}

  register_routes(app)
  
  app.mount("/static", StaticFiles(directory="app/static"), name="static")
  return app

app = create_app()
