from fastapi import FastAPI

from starlette.middleware.cors import CORSMiddleware
from routers import auth_user, user

app = FastAPI()

app.include_router(auth_user.router)
app.include_router(user.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
