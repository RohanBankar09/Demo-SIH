from app.core.database import engine
from app.models.base import Base

from app.models import (  # noqa: F401
    Application,
    ApplicationStatusHistory,
    Assessment,
    AssessmentAnswer,
    AssessmentAttempt,
    AssessmentQuestion,
    IndustryProfile,
    Opportunity,
    OpportunitySkill,
    QuestionOption,
    Skill,
    StudentProfile,
    StudentSkill,
    User,
)


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_tables()
    print("PIXIE database tables created successfully.")