
from fastapi import FastAPI

from fast_zero.routers import auth, users, videos, challenges, quiz

app = FastAPI(title="EduRecode API")

app.include_router(auth.router) 
app.include_router(users.router)         # já usa /users
app.include_router(videos.router)        # /videos
app.include_router(challenges.router)    # /challenges
app.include_router(quiz.router)          # /quiz