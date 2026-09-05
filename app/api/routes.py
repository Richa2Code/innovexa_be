from fastapi import APIRouter
from app.api.user_routes import router as user_router
from app.api.public_routes import router as public_router

app_router = APIRouter()

app_router.include_router(user_router)
app_router.include_router(public_router)
