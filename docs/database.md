# Database

SQLite stores the demo learning platform.

Core entities:

- `User` and `UserStats`
- `Language`
- `Course`, `Unit`, `Skill`, `Lesson`, `Exercise`
- `ExerciseOption` and `MatchPair`
- `UserCourseProgress`, `UserSkillProgress`, `UserLessonProgress`, `UserExerciseProgress`
- `Quest`, `UserQuestProgress`
- `Achievement`, `UserAchievement`
- `LeaderboardEntry`

Run the seed script with:

```bash
$env:PYTHONPATH="backend"; python -m app.seed
```

The seed is deterministic and safe to rerun against an already-seeded database.
