from fastapi import FastAPI
from router import initialize
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()
app.include_router(initialize.router)

origins = [
    os.getenv("API_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_credentials = True
)

@app.get("/")
def index():
    return {"status":200}