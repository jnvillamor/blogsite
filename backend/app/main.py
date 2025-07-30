from fastapi import FastAPI
from app.api.v1 import register_routes

def create_app() -> FastAPI:
  app = FastAPI(title="Blogsite API")

  @app.get("/")
  def root():
    return {"message": "Welcome to the Blogsite API"}

  register_routes(app)

  return app

app = create_app()
