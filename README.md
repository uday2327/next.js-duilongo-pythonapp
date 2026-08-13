# Duolingo Web App Clone

## Overview

This is a full-stack Duolingo-inspired learning app for English practice by Hindi speakers. It opens with a data-driven language-selection screen, then continues into a guided learning path, locked and completed lessons, varied exercise types, hearts, XP, streaks, quests, leaderboard, shop, profile, pronunciation practice, seeded SQLite data, and persistent progress through a FastAPI backend.

The default learner is **Uday Dixit** (`username: Uday`).

## Simple Architecture

This project intentionally uses a simple monolithic architecture because the assignment has a small seeded dataset and a single primary learner. The architecture separates UI, API routes, business logic and database models while avoiding unnecessary enterprise abstractions. This keeps the code easy to understand, maintain and demonstrate during evaluation.

The project is divided into two simple parts: a Next.js frontend and a FastAPI backend. The frontend contains pages and reusable UI components. Pages fetch data through a small API client, while components focus mainly on presentation and interaction. The FastAPI backend has routes for HTTP endpoints, services for business logic, SQLAlchemy models for database access, and SQLite for persistence. Lesson completion is handled by the lesson service, while XP, hearts, streaks, quests and achievements are handled by the gamification service. Learning path unlocking is handled by the progression service.

```text
Next.js Frontend
      |
   REST API
      |
 FastAPI Routes
      |
   Services
      |
SQLAlchemy Models
      |
    SQLite
```

## Features

- Duolingo-style learning path with unit headers, organic node layout, locked lessons, available lessons, completed lessons, and skill progress.
- Home page language selection with searchable ISO 639-1 language catalog from SQLite.
- Separate language catalog and course availability check, so unsupported language pairs show coming soon.
- Lesson player with multiple choice, fill blank, translation, word bank, type answer, and match pairs.
- Backend answer validation with normalized text comparison.
- Hearts decrease on wrong answers and regenerate server-side over time.
- Lesson completion persists XP, streak, daily goal progress, quests, achievements, leaderboard XP, and skill progress.
- Pages for Learn, Lesson, Characters, Leaderboard, Quests, Shop, Profile, and Settings.
- Seeded course: English for Hindi Speakers, with 4 units, 16 skills, 48 lessons, and varied exercises.

## Tech Stack

- Frontend: Next.js App Router, TypeScript, React, Tailwind CSS, lucide-react
- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic, Uvicorn
- Testing: pytest for core backend rules

## Project Structure

```text
frontend/
  src/app/              Next.js routes
  src/components/       Reusable UI pieces
  src/lib/api.ts        Single frontend API client
  src/types/index.ts    Shared frontend types

backend/
  app/main.py           FastAPI setup and router registration
  app/database.py       SQLite engine and session
  app/models.py         SQLAlchemy models
  app/schemas.py        Request/response schemas
  app/routes/           Thin HTTP route handlers
  app/services/         Lesson, gamification, progression logic
  app/seed.py           Deterministic seed script
```

## Local Setup

Install frontend dependencies:

```bash
cd frontend
npm install
```

Install backend dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

Seed the database:

```bash
$env:PYTHONPATH="backend"; python -m app.seed
```

Run the backend:

```bash
cd backend
$env:PYTHONPATH="."; python -m uvicorn app.main:app --reload --port 8000
```

Run the frontend in another terminal:

```bash
cd frontend
npm run dev
```

Open `http://localhost:3000`.

## Environment Variables

Root `.env.example` and `backend/.env.example` are included.

- `NEXT_PUBLIC_API_URL=http://localhost:8000`
- `DATABASE_URL=sqlite:///./duolingo_clone.db`
- `FRONTEND_URL=http://localhost:3000`
- `ENVIRONMENT=development`
- `SECRET_KEY=development-only-change-me`

## API Overview

- `GET /api/me`
- `GET /languages`
- `GET /api/languages`
- `GET /api/languages/course-status?base=hi&target=en`
- `GET /api/stats`
- `POST /api/stats/goal`
- `POST /api/stats/shop`
- `GET /api/learn`
- `GET /api/lessons/{lesson_id}`
- `POST /api/exercises/{exercise_id}/answer`
- `POST /api/lessons/{lesson_id}/complete`
- `GET /api/quests`
- `GET /api/leaderboard`
- `GET /api/profile`
- `GET /api/characters`

## Testing

Run backend tests:

```bash
$env:PYTHONPATH="backend"; python -m pytest backend/tests -q
```

Run frontend production build:

```bash
cd frontend
npm run build
```

Verified locally:

- `npm run build`
- `python -m pytest backend/tests -q`
- database seed script
- key API endpoints with FastAPI TestClient

## Assumptions

- Authentication is simplified to one default learner, Uday Dixit.
- Purchases are mocked and use seeded gems.
- Speech on the Characters page uses the browser `speechSynthesis` API when available.
- SQLite is appropriate for the assignment demo; deployment should use persistent disk if hosted.
