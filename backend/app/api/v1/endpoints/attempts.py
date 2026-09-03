from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.v1.endpoints.student import get_current_user
from app.core.database import get_db
from app.models.assessment import Assessment
from app.models.assessment_answer import AssessmentAnswer
from app.models.assessment_attempt import AssessmentAttempt
from app.models.assessment_question import AssessmentQuestion
from app.models.question_option import QuestionOption
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.attempt import (
    AttemptResponse,
    AttemptResultResponse,
    AttemptStart,
    AttemptSubmit,
)


router = APIRouter(
    prefix="/attempts",
    tags=["Assessment Attempts"],
)


def get_current_student(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> StudentProfile:
    if current_user.role != "student":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only students can perform this action",
        )

    student = (
        db.query(StudentProfile)
        .filter(StudentProfile.user_id == current_user.id)
        .first()
    )

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student profile not found",
        )

    return student


@router.post(
    "/start",
    response_model=AttemptResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_attempt(
    attempt_data: AttemptStart,
    current_student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    assessment = db.get(
        Assessment,
        attempt_data.assessment_id,
    )

    if not assessment or not assessment.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found",
        )

    existing_attempt = (
        db.query(AssessmentAttempt)
        .filter(
            AssessmentAttempt.student_id == current_student.id,
            AssessmentAttempt.assessment_id == attempt_data.assessment_id,
            AssessmentAttempt.status == "in_progress",
        )
        .first()
    )

    if existing_attempt:
        return existing_attempt

    questions = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id == attempt_data.assessment_id
        )
        .all()
    )

    if not questions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment has no questions",
        )

    max_score = sum(
        question.marks
        for question in questions
    )

    attempt = AssessmentAttempt(
        student_id=current_student.id,
        assessment_id=attempt_data.assessment_id,
        status="in_progress",
        max_score=max_score,
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.get(
    "/me",
    response_model=list[AttemptResultResponse],
)
@router.get(
    "/my",
    response_model=list[AttemptResultResponse],
)
def get_my_attempts(
    current_student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    attempts = (
        db.query(AssessmentAttempt)
        .filter(AssessmentAttempt.student_id == current_student.id)
        .order_by(AssessmentAttempt.id.desc())
        .all()
    )

    results = []
    for attempt in attempts:
        assessment = db.get(Assessment, attempt.assessment_id)
        assessment_title = assessment.title if assessment else None
        results.append({
            "attempt_id": attempt.id,
            "assessment_id": attempt.assessment_id,
            "assessment_title": assessment_title,
            "status": attempt.status,
            "score": attempt.score,
            "max_score": attempt.max_score,
            "percentage": attempt.percentage,
            "completed_at": attempt.completed_at,
        })

    return results


@router.post(
    "/{attempt_id}/submit",
    response_model=AttemptResponse,
)
def submit_attempt(
    attempt_id: int,
    submission: AttemptSubmit,
    current_student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    attempt = db.get(
        AssessmentAttempt,
        attempt_id,
    )

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    if attempt.student_id != current_student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to submit this attempt",
        )

    if attempt.status != "in_progress":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt has already been submitted",
        )

    questions = (
        db.query(AssessmentQuestion)
        .filter(
            AssessmentQuestion.assessment_id
            == attempt.assessment_id
        )
        .all()
    )

    question_map = {
        question.id: question
        for question in questions
    }

    seen_question_ids = set()
    answers_to_create = []
    total_score = 0

    for submitted_answer in submission.answers:
        if submitted_answer.question_id in seen_question_ids:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Duplicate answer for question {submitted_answer.question_id}",
            )
        seen_question_ids.add(submitted_answer.question_id)

        question = question_map.get(
            submitted_answer.question_id
        )

        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=(
                    f"Question "
                    f"{submitted_answer.question_id} "
                    f"does not belong to this assessment"
                ),
            )

        selected_option = None

        if submitted_answer.selected_option_id:
            selected_option = db.get(
                QuestionOption,
                submitted_answer.selected_option_id,
            )

            if not selected_option:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Selected option {submitted_answer.selected_option_id} not found",
                )

            if selected_option.question_id != question.id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Option {submitted_answer.selected_option_id} does not belong to question {question.id}",
                )

        is_correct = (
            selected_option is not None
            and selected_option.is_correct
        )

        marks_awarded = (
            question.marks
            if is_correct
            else 0
        )

        total_score += marks_awarded

        answers_to_create.append(
            AssessmentAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                selected_option_id=(
                    selected_option.id
                    if selected_option
                    else None
                ),
                answer_text=submitted_answer.answer_text,
                is_correct=is_correct,
                marks_awarded=marks_awarded,
            )
        )

    # Atomically persist answers and update attempt
    for answer in answers_to_create:
        db.add(answer)

    max_score = attempt.max_score or 0

    percentage = (
        round((total_score / max_score) * 100)
        if max_score > 0
        else 0
    )

    attempt.score = total_score
    attempt.percentage = percentage
    attempt.status = "completed"
    attempt.completed_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(attempt)

    return attempt


@router.get(
    "/{attempt_id}/result",
    response_model=AttemptResultResponse,
)
def get_attempt_result(
    attempt_id: int,
    current_student: StudentProfile = Depends(get_current_student),
    db: Session = Depends(get_db),
):
    attempt = db.get(
        AssessmentAttempt,
        attempt_id,
    )

    if not attempt:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Attempt not found",
        )

    if attempt.student_id != current_student.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to view this result",
        )

    if attempt.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Attempt is still in progress. Please submit the assessment first.",
        )

    assessment = db.get(Assessment, attempt.assessment_id)
    assessment_title = assessment.title if assessment else None

    return {
        "attempt_id": attempt.id,
        "assessment_id": attempt.assessment_id,
        "assessment_title": assessment_title,
        "status": attempt.status,
        "score": attempt.score,
        "max_score": attempt.max_score,
        "percentage": attempt.percentage,
        "completed_at": attempt.completed_at,
    }