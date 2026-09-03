from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.assessment import Assessment
from app.models.assessment_question import AssessmentQuestion
from app.models.skill import Skill
from app.schemas.assessment import AssessmentCreate, AssessmentResponse
from app.schemas.question import QuestionResponse


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post(
    "/",
    response_model=AssessmentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_assessment(
    assessment_data: AssessmentCreate,
    db: Session = Depends(get_db),
):
    skill = db.get(Skill, assessment_data.skill_id)

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found",
        )

    assessment = Assessment(
        skill_id=assessment_data.skill_id,
        title=assessment_data.title,
        description=assessment_data.description,
        difficulty=assessment_data.difficulty,
        time_limit_minutes=assessment_data.time_limit_minutes,
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment


@router.get(
    "/",
    response_model=list[AssessmentResponse],
)
def list_assessments(
    db: Session = Depends(get_db),
):
    return (
        db.query(Assessment)
        .filter(Assessment.is_active.is_(True))
        .order_by(Assessment.id)
        .all()
    )


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
)
def get_assessment(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assessment = db.get(Assessment, assessment_id)

    if not assessment or not assessment.is_active:
        raise HTTPException(
            status_code=404,
            detail="Assessment not found",
        )

    return assessment


@router.get(
    "/{assessment_id}/questions",
    response_model=list[QuestionResponse],
)
def get_assessment_questions(
    assessment_id: int,
    db: Session = Depends(get_db),
):
    assessment = db.get(Assessment, assessment_id)

    if not assessment or not assessment.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    questions = (
        db.query(AssessmentQuestion)
        .options(selectinload(AssessmentQuestion.options))
        .filter(AssessmentQuestion.assessment_id == assessment_id)
        .order_by(AssessmentQuestion.order_index)
        .all()
    )

    return questions