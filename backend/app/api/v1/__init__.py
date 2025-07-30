from fastapi import FastAPI
from app.api.v1.user_endpoint import router as user_router

def register_routes(app: FastAPI):
  app.include_router(user_router, prefix="/api/v1", tags=["v1"])
  