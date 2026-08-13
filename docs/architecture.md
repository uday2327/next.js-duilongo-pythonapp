# Architecture

The app keeps a small, interview-friendly structure:

- Next.js pages load data and compose UI components.
- `frontend/src/lib/api.ts` contains all frontend API calls.
- FastAPI routes receive requests and call one of three services.
- `lesson_service.py` handles answer validation and lesson completion.
- `gamification_service.py` handles XP, hearts, streaks, quests, achievements, and leaderboard updates.
- `progression_service.py` handles path and lesson unlocking.
- `models.py` contains all SQLAlchemy models in one readable file.

This keeps each important user action easy to trace from browser click to SQLite update.
