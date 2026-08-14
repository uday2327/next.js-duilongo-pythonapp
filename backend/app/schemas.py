from pydantic import BaseModel, Field


class AnswerRequest(BaseModel):
    answer: str | list[str] | dict[str, str]


class CompleteLessonRequest(BaseModel):
    score: int = Field(ge=0, le=100)
    mistakes: int = Field(ge=0)
    correct_count: int = Field(ge=0)
    total_count: int = Field(gt=0)


class GoalRequest(BaseModel):
    daily_goal: int = Field(ge=1, le=100)


class SelectCourseRequest(BaseModel):
    course_id: int = Field(gt=0)


class ExerciseOptionOut(BaseModel):
    id: int
    text: str
    is_correct: bool


class MatchPairOut(BaseModel):
    id: int
    left_text: str
    right_text: str


class ExerciseOut(BaseModel):
    id: int
    type: str
    prompt: str
    instruction: str
    correct_answer: str
    explanation: str
    options: list[ExerciseOptionOut] = []
    pairs: list[MatchPairOut] = []


class LessonOut(BaseModel):
    id: int
    title: str
    xp_reward: int
    estimated_minutes: int
    hearts: int
    exercises: list[ExerciseOut]


class RefillRequest(BaseModel):
    item: str = "heart_refill"
