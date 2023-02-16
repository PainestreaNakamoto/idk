from fastapi import APIRouter
from app.endpoint import auth, spotify

router = APIRouter()

router.include_router(spotify.router, prefix="/spotify")
router.include_router(auth.router, prefix="/auth")

