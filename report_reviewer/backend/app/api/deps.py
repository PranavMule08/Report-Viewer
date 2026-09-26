from fastapi import APIRouter

from app.api import auth, reports, reviews, chat, upload

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
api_router.include_router(upload.router, prefix="/upload", tags=["File Upload"])
api_router.include_router(reports.router, prefix="/reports", tags=["Reports"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
