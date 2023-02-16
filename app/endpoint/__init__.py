from fastapi import APIRouter
from app.endpoint import auth, spotify

router = APIRouter()

router.include_router(spotify.router,tags=["Spotify"])
router.include_router(auth.router, prefix="/auth", tags=["Auth"])

