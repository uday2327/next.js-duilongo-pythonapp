import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.routes import courses, languages, leaderboard, lessons, quests, stats, users

app = FastAPI(title="Duolingo Clone API")

frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/api/health")
def health():
    return {"ok": True}


app.include_router(users.router)
app.include_router(languages.router)
app.include_router(courses.router)
app.include_router(lessons.router)
app.include_router(stats.router)
app.include_router(quests.router)
app.include_router(leaderboard.router)
