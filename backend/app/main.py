from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import register_routes

def create_app() -> FastAPI:
  app = FastAPI(title="Blogsite API")

  @app.get("/")
  def root():
    return {"message": "Welcome to the Blogsite API"}

  register_routes(app)
  
  app.mount("/static", StaticFiles(directory="app/static"), name="static")
  return app

app = create_app()
