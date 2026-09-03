from pydantic import BaseModel, Field


class AssessmentCreate(BaseModel):
    skill_id: int
    title: str = Field(min_length=3, max_length=200)
    description: str | None = None
    difficulty: str = "beginner"
    time_limit_minutes: int | None = Field(default=None, gt=0)


class AssessmentResponse(BaseModel):
    id: int
    skill_id: int
    title: str
    description: str | None
    difficulty: str
    time_limit_minutes: int | None
    is_active: bool

    model_config = {"from_attributes": True}