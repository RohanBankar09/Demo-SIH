from pydantic import BaseModel, Field


class QuestionOptionCreate(BaseModel):
    option_text: str = Field(min_length=1, max_length=500)
    is_correct: bool = False
    order_index: int = Field(ge=0)


class QuestionCreate(BaseModel):
    assessment_id: int
    question_text: str = Field(min_length=5)
    question_type: str = "mcq"
    difficulty: str = "beginner"
    marks: int = Field(default=1, gt=0)
    order_index: int = Field(ge=0)
    options: list[QuestionOptionCreate]


class QuestionOptionResponse(BaseModel):
    id: int
    option_text: str
    order_index: int

    model_config = {"from_attributes": True}


class QuestionResponse(BaseModel):
    id: int
    assessment_id: int
    question_text: str
    question_type: str
    difficulty: str
    marks: int
    order_index: int
    options: list[QuestionOptionResponse]

    model_config = {"from_attributes": True}