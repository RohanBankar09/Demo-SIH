from datetime import datetime

from pydantic import BaseModel


class AttemptStart(BaseModel):
    assessment_id: int
    student_id: int | None = None


class AnswerSubmit(BaseModel):
    question_id: int
    selected_option_id: int | None = None
    answer_text: str | None = None


class AttemptSubmit(BaseModel):
    answers: list[AnswerSubmit]


class AttemptResponse(BaseModel):
    id: int
    student_id: int
    assessment_id: int
    status: str
    score: int | None = None
    max_score: int | None = None
    percentage: int | None = None

    model_config = {"from_attributes": True}


class AttemptResultResponse(BaseModel):
    attempt_id: int
    assessment_id: int
    assessment_title: str | None = None
    status: str
    score: int | None = None
    max_score: int | None = None
    percentage: int | None = None
    completed_at: datetime | None = None

    model_config = {"from_attributes": True}