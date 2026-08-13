# API

The frontend talks to the backend through REST endpoints under `/api`.

- `GET /api/learn`: course, units, skills, lessons, and progression state
- `GET /languages` and `GET /api/languages`: searchable language catalog
- `GET /api/languages/course-status?base=hi&target=en`: checks whether a selected language pair has seeded course content
- `GET /api/lessons/{id}`: lesson exercises and current hearts
- `POST /api/exercises/{id}/answer`: validates one exercise answer
- `POST /api/lessons/{id}/complete`: persists lesson completion and rewards
- `GET /api/stats`: XP, hearts, gems, streak, and daily goal
- `POST /api/stats/goal`: updates the daily XP goal
- `POST /api/stats/shop`: buys mocked shop items
- `GET /api/quests`: daily quest progress
- `GET /api/leaderboard`: weekly leaderboard
- `GET /api/profile`: profile stats and achievements
