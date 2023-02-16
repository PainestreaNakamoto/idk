from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.models import User
from app.database import get_db
from app.endpoint import auth, spotify
from sqlalchemy.orm import Session
from jose import jwt
from app.services import spotify , login

router = APIRouter()


templates = Jinja2Templates(directory="app/templates")

def verify_jwt_token(token,db):
    try:
        payload = jwt.decode(token,"helloworldkey")
        username = payload.get("sub")
        if username is None:
            print("her")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")
        user = db.query(User).filter(User.email==username).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unable to verify credentials")

@router.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    token = request.cookies.get("accees_token")
    if token is None:
        print(token)
        return templates.TemplateResponse("index.html", {"request": request, "errors": "Please login"})
    spotify_obj = spotify.SpotifyService()
    items = spotify_obj.all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items, "is_login": True})

@router.get("/ei", response_class=HTMLResponse)
async def read_item(request: Request):
    spotify_obj = spotify.SpotifyService()
    items = spotify_obj.all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items, "is_login": True})

@router.get("/api")
async def read_item(token: str = Depends(login.oauth2_scheme), db: Session = Depends(get_db)):
    verify_jwt_token(token,db)
    spotify_obj = spotify.SpotifyService()
    items = spotify_obj.all()
    return items

