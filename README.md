# Lingo: Duolingo-Inspired Learning App

## Project Overview

Lingo is a small full-stack language-learning application built for an SDE assignment. It teaches English to Hindi speakers through a Duolingo-style learning path, short lessons, immediate answer feedback, XP, hearts, streaks, quests, achievements, and a leaderboard.

The project deliberately uses one simple frontend, one simple API, and SQLite. There are no microservices, external authentication providers, or cloud database dependencies to explain in an interview.

The seeded learner is **Uday Dixit**. The optional visual login screen accepts `abc@gmail.com` with password `3214`; authentication is intentionally simplified for this assignment.

## Features

- Data-driven learning path with units, skills, completed lessons, the next available lesson, and locked lessons.
- Lesson player with eight exercises per lesson:
  - multiple choice
  - word-bank translation
  - match pairs
  - fill in the blank
  - typed answer
- Immediate correct and incorrect feedback, lesson progress, heart loss on wrong answers, and an out-of-hearts state.
- Persistent lesson completion, skill progress, XP, daily-goal progress, streaks, quests, achievements, and leaderboard XP.
- Hearts regenerate on the backend every 30 minutes; the shop also provides a mock heart refill for gems.
- Seeded English-for-Hindi-speakers course with 4 units, 16 skills, 48 lessons, and 384 exercises.
- API-backed language selection, profile, leaderboard, quests, character pronunciation practice, shop, and settings placeholder.
- Responsive path and navigation layouts, loading state, route transitions, and clear locked/completed visual states.

## Tech Stack

| Area | Technology | Why it is used |
| --- | --- | --- |
| Frontend | Next.js App Router, React, TypeScript | Pages, routing, typed UI, and client-side lesson interaction. |
| Styling | Tailwind CSS and small CSS theme helpers | Fast, consistent Duolingo-inspired UI styling. |
| UI helpers | lucide-react and framer-motion | Icons and lightweight route motion. |
| Backend | FastAPI and Pydantic | Small REST API with validated request bodies. |
| Data access | SQLAlchemy | Readable Python models and database queries. |
| Database | SQLite | Persistent local data with no service to configure. |
| Tests | pytest | Tests the core streak, XP, heart, quest, and unlock rules. |

## Simple Architecture

```text
Browser
  |
  v
Next.js frontend
  |
  | fetch() REST requests
  v
FastAPI routes
  |
  v
Small service functions
  |
  v
SQLAlchemy models
  |
  v
SQLite database file
```

The frontend keeps API calls in `frontend/src/lib/api.ts`. Pages use that file to request data and pass it into reusable components. FastAPI route files handle HTTP concerns, while three small service files contain the rules for lessons, gamification, and progression. SQLAlchemy models are the only layer that reads or writes SQLite.

### Main Request Flow

```text
User answers an exercise
  -> POST /api/exercises/{exercise_id}/answer
  -> lesson_service validates the answer
  -> UserExerciseProgress and UserStats are updated in SQLite
  -> API returns correct/incorrect, expected answer, and current hearts
  -> LessonPlayer shows feedback immediately
```

When a lesson is completed, `lesson_service` records lesson and skill progress. `gamification_service` awards XP, updates the streak and daily goal, updates quests and achievements, and reranks the leaderboard.

## Important Pages

| Route | What it does |
| --- | --- |
| `/` | Language/course selection. A learner with an already selected course is sent back to `/learn`. |
| `/login` | Optional visual demo login; real authentication is intentionally out of scope. |
| `/learn` | Main learning path with units, lesson nodes, daily goal, quest, and leaderboard preview. |
| `/lesson/[id]` | Lesson player, progress bar, feedback bar, completion state, and out-of-hearts state. |
| `/profile` | Learner name, XP, streak, completed lessons/skills, and achievements. |
| `/leaderboard` | Seeded weekly leaderboard. |
| `/quests` | Backend-backed daily quest progress. |
| `/shop` | Mock heart refill using gems. |
| `/characters` | Browser speech-synthesis pronunciation practice. |
| `/settings` | UI placeholder for future preference persistence. |

## Project Structure

```text
frontend/
  src/app/                 Next.js routes and pages
  src/components/          Reusable path, lesson, header, and navigation UI
  src/lib/api.ts           One typed REST client for all frontend requests
  src/types/               Frontend data shapes
  .env.example             Frontend environment-variable template

backend/
  app/main.py              FastAPI setup, CORS, startup seeding, router registration
  app/database.py          SQLite engine, session factory, local .env loading
  app/models.py            SQLAlchemy table definitions
  app/schemas.py           Pydantic request validation
  app/routes/              Small route handlers grouped by feature
  app/services/            Lesson, gamification, and progression rules
  app/seed.py              Idempotent demo-data seed script
  tests/                   Backend rule tests
  .env.example             Backend environment-variable template

docs/                      Supplementary API, architecture, and database notes
```

## Database Design

The schema is normalized enough for the assignment while keeping each table easy to explain.

```text
Course -> Unit -> Skill -> Lesson -> Exercise
                                     |     |
                              ExerciseOption MatchPair

User -> UserStats
User -> UserCourseProgress -> Course
User -> UserSkillProgress  -> Skill
User -> UserLessonProgress -> Lesson
User -> UserExerciseProgress -> Exercise

User -> UserQuestProgress -> Quest
User -> UserAchievement -> Achievement
User -> LeaderboardEntry
```

| Table group | Purpose |
| --- | --- |
| `users`, `user_stats` | The seeded learner and durable XP, streak, hearts, gems, daily goal, and heart regeneration timestamp. |
| `languages`, `courses`, `units`, `skills`, `lessons` | The course hierarchy that creates the learning path. |
| `exercises`, `exercise_options`, `match_pairs` | Exercise prompts, accepted answers, selectable options, and matching data. |
| `user_course_progress`, `user_skill_progress`, `user_lesson_progress`, `user_exercise_progress` | Persistent learner progress at the course, skill, lesson, and exercise levels. |
| `quests`, `user_quest_progress` | Seeded daily quest definitions and per-user progress. |
| `achievements`, `user_achievements` | Achievement definitions and unlocked records. |
| `leaderboard_entries` | Seeded weekly XP display data. |

SQLite is the final database. Startup and the seed command are idempotent: they create missing tables/content but do not erase existing learner progress.

## API Overview

All API routes are served by FastAPI. The frontend uses the `/api/...` forms below.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Health check. |
| GET | `/api/me` | Default learner, stats, and selected course. |
| GET | `/api/profile` | Profile summary and achievements. |
| POST | `/api/select-course` | Save the selected seeded course. |
| GET | `/api/languages` | Searchable language catalog. `/languages` is a compatible alias. |
| GET | `/api/languages/course-status?base=hi&target=en` | Check whether a course pair is available. |
| GET | `/api/learn` | Course path with unit, skill, lesson, and lock-state data. |
| GET | `/api/lessons/{lesson_id}` | Load an unlocked lesson unless the learner is out of hearts. |
| POST | `/api/exercises/{exercise_id}/answer` | Validate an answer and update heart/exercise progress. |
| POST | `/api/lessons/{lesson_id}/complete` | Persist completed lesson, XP, path progress, goals, quests, achievements, and leaderboard. |
| GET | `/api/stats` | Current XP, streak, hearts, gems, and daily goal. |
| POST | `/api/stats/goal` | Set a daily goal from 1 through 100 XP. |
| POST | `/api/stats/shop` | Use the mock heart refill. |
| GET | `/api/quests` | Current quest data. |
| GET | `/api/leaderboard` | Seeded weekly leaderboard. |
| GET | `/api/characters` | Pronunciation-card content. |

## Environment Variables

Copy the matching example files. Real `.env` and `.env.local` files are ignored by Git.

### Frontend: `frontend/.env.local`

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Use the deployed FastAPI URL in production, for example `https://your-api.onrender.com`. This value is public by design because it is compiled into the browser bundle.

### Backend: `backend/.env`

```env
DATABASE_URL=sqlite:///./duolingo_clone.db
FRONTEND_URL=http://localhost:3000
```

`DATABASE_URL` is the only database setting used by the backend. `FRONTEND_URL` is the allowed browser origin for CORS. Do not add an old Supabase/PostgreSQL connection string: this assignment uses SQLite.

## Run Locally

These commands are for PowerShell from a clean machine.

### 1. Start the backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
python -m app.seed
python -m uvicorn app.main:app --reload --port 8000
```

`python -m app.seed` can be run at any time. The FastAPI startup hook also seeds a fresh SQLite file automatically, so it is safe if the command was already run.

### 2. Start the frontend in a second terminal

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

Open `http://localhost:3000`.

## Testing and Build

From the repository root:

```powershell
$env:PYTHONPATH="backend"
python -m pytest backend/tests -q
```

From `frontend/`:

```powershell
npm run lint
npm run build
```

## Deployment

The simplest assignment deployment is a Vercel frontend plus a Render or Railway FastAPI service. SQLite must be placed on a persistent disk/volume. A serverless or ephemeral filesystem will reset learner progress after a restart.

### 1. Push the source to a public GitHub repository

```powershell
git add .
git commit -m "Prepare Lingo assignment for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_GITHUB_USER/lingo-assignment.git
git push -u origin main
```

Do not add `backend/venv/`, `.env`, `.env.local`, or SQLite database files. They are ignored already.

### 2. Deploy the backend on Render

Create a Render **Web Service** from the repository with these settings:

```text
Root Directory: backend
Build Command: pip install -r requirements.txt
Start Command: python -m uvicorn app.main:app --host 0.0.0.0 --port $PORT
Persistent Disk Mount Path: /var/data
```

Set these environment variables in Render:

```text
DATABASE_URL=sqlite:////var/data/duolingo_clone.db
FRONTEND_URL=https://YOUR-VERCEL-PROJECT.vercel.app
```

The app seeds the mounted database automatically during its first startup. Test `https://YOUR-API.onrender.com/api/health` after deployment.

### 3. Deploy the frontend on Vercel

Set the Vercel project root directory to `frontend`. Add this production environment variable before the production build:

```text
NEXT_PUBLIC_API_URL=https://YOUR-API.onrender.com
```

Then deploy with the Vercel CLI, or import the repository in the Vercel dashboard:

```powershell
cd frontend
npm install --global vercel
vercel login
vercel --prod
```

If the backend URL changes, update `NEXT_PUBLIC_API_URL` in Vercel and redeploy because Next.js exposes it to the browser at build time.

### Railway Alternative

Railway works with the same backend root and start command. Attach a volume mounted at `/data`, then set:

```text
DATABASE_URL=sqlite:////data/duolingo_clone.db
FRONTEND_URL=https://YOUR-VERCEL-PROJECT.vercel.app
```

## Design Decisions

- One FastAPI app is easier to read and demonstrate than multiple services.
- One `api.ts` frontend client prevents API URLs and JSON handling from being duplicated across pages.
- Three focused backend services keep route functions short without hiding logic behind extra layers.
- SQLite is ideal for the assignment and local demo. Persistent disk is required when hosting it.
- Authentication, subscriptions, social features, audio files, and multi-language course content are intentionally simplified because they are outside the required learning workflow.

## Assumptions and Future Improvements

The app assumes a default seeded learner and one fully available Hindi-to-English course. Gems, shop purchases, leaderboard users, and login are demo data. Browser speech synthesis is optional and depends on browser support.

Reasonable next steps outside the assignment scope would be real authentication, persistent settings, audio recordings, additional authored courses, server-side lesson attempts, and a managed database for larger multi-user traffic.
