from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.endpoint import router
from app import models, database, services

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
