from fastapi import FastAPI
from app.api.v1.auth_endpoint import router as auth_router
from app.api.v1.blog_endpoint import router as blog_router
from app.api.v1.comment_endpoint import router as comment_router
from app.api.v1.user_endpoint import router as user_router

def register_routes(app: FastAPI):
  app.include_router(auth_router, prefix="/api/v1", tags=["v1"])
  app.include_router(blog_router, prefix="/api/v1", tags=["v1"])
  app.include_router(comment_router, prefix="/api/v1", tags=["v1"])
  app.include_router(user_router, prefix="/api/v1", tags=["v1"])
  