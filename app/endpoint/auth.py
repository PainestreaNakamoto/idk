from fastapi import APIRouter, Request, Depends, status , HTTPException, Response
from jose import jwt
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.endpoint import auth, spotify
from app.models import User
from app.services import hanshing as hashing
from app.database import get_db
from typing import List
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from fastapi.responses import RedirectResponse

router = APIRouter()

templates = Jinja2Templates(directory="app/templates")

class AuthRegisterRequestForm(BaseModel):
    email: EmailStr
    password: str

class AuthResponse(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

@router.post("/login/token")
async def retireve_token_after_authentication(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid username")
    if not hashing.Hasher.verify_password(form_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid password")
    data = {"sub": form_data.username,"issuer": user.id}
    jwt_token = jwt.encode(data,"helloworldkey",algorithm="HS256")

    return {"access_token": jwt_token,"token_type": "bearer"}

@router.get("/login")
async def login(request: Request):
    if request.cookies.get("accees_token"):
        return RedirectResponse("/")

    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, response: Response ,db: Session = Depends(get_db)):
    username = await request.form()
    if request.cookies.get("accees_token"):
        return RedirectResponse("/")
    if not username.get("email"):
        return templates.TemplateResponse("login.html", {"request": request,"errors":"Please enter email"})
    if not username.get("password"):
        return templates.TemplateResponse("login.html", {"request": request,"errors":"Please enter password"})
    try:
        user = db.query(User).filter(User.email==username.get("email")).first()
        if user is None:
            return templates.TemplateResponse("login.html", {"request": request,"errors":"Email does not exits"})
        if not hashing.Hasher.verify_password(username.get("password"),user.password):
            return templates.TemplateResponse("login.html", {"request": request,"errors":"Password is incorrect"})
        data = {"sub": user.email}
        jwt_token = jwt.encode(data,"helloworldkey",algorithm="HS256")
        response = templates.TemplateResponse("login.html", {"request": request,"ok": "login successfully","is_login": True})
        response.set_cookie(key="accees_token",value=f"Bearer {jwt_token}",httponly=True)
        return response
    except Exception as e:
        print(e)
        return templates.TemplateResponse("login.html", {"request": request, "errors": "something wrong"})
            

@router.get("/register")
async def register(request: Request, response: Response):
    if request.cookies.get("accees_token"):
        return RedirectResponse("/")
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
async def register(request: Request,db: Session = Depends(get_db)):
    user = await request.form()

    if request.cookies.get("accees_token"):
        return RedirectResponse("/")


    if len(user.get("password")) < 6:
        errors = "password must be > 6 characters"
        return templates.TemplateResponse("register.html", {"request": request,"errors": errors})
    
    try:
        new_user = User(email=user.get("email"),password=hashing.Hasher.get_hash_password(user.get("password")))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        print("here")
        errors = "Email already exits"
        return templates.TemplateResponse("register.html", {"request": request,"errors": errors})

    data = {"sub": user.get("email")}
    jwt_token = jwt.encode(data,"helloworldkey",algorithm="HS256")
    response =  templates.TemplateResponse("register.html", {"request": request,"ok": "Register successfully","is_login": True})
    response.set_cookie(key="accees_token",value=f"Bearer {jwt_token}",httponly=True)
    return response

