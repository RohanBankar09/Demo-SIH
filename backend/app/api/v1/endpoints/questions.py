from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.question_option import QuestionOption
from app.schemas.question import QuestionCreate, QuestionResponse


router = APIRouter(
    prefix="/questions",
    tags=["Assessment Questions"],
)


@router.get(
    "/",
    response_model=list[QuestionResponse],
)
def list_questions(
    assessment_id: int | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(AssessmentQuestion).options(selectinload(AssessmentQuestion.options))
    if assessment_id is not None:
        query = query.filter(AssessmentQuestion.assessment_id == assessment_id)
    return query.order_by(AssessmentQuestion.order_index).all()


@router.post(
    "/",
    response_model=QuestionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_question(
    question_data: QuestionCreate,
    db: Session = Depends(get_db),
):
    assessment = db.get(
        Assessment,
        question_data.assessment_id,
    )

    if not assessment:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    if not question_data.options:
        raise HTTPException(
            status_code=400,
            detail="At least one option is required",
        )

    correct_count = sum(
        option.is_correct
        for option in question_data.options
    )

    if question_data.question_type == "mcq" and correct_count != 1:
        raise HTTPException(
            status_code=400,
            detail="MCQ must have exactly one correct option",
        )

    question = AssessmentQuestion(
        assessment_id=question_data.assessment_id,
        question_text=question_data.question_text,
        question_type=question_data.question_type,
        difficulty=question_data.difficulty,
        marks=question_data.marks,
        order_index=question_data.order_index,
    )

    db.add(question)
    db.flush()

    for option_data in question_data.options:
        option = QuestionOption(
            question_id=question.id,
            option_text=option_data.option_text,
            is_correct=option_data.is_correct,
            order_index=option_data.order_index,
        )

        db.add(option)

    db.commit()
    db.refresh(question)

    return question