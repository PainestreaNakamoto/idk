from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
import requests
from fastapi.middleware.cors import CORSMiddleware
from math import floor
from services import spotify

app = FastAPI()

origins = [
"*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    spotify_obj = spotify.SpotifyService()
    items = spotify_obj.all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


