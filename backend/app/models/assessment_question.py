from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessments.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    question_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="mcq",
    )

    difficulty: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="beginner",
    )

    marks: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    order_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    options: Mapped[list["QuestionOption"]] = relationship(
        "QuestionOption",
        cascade="all, delete-orphan",
        order_by="QuestionOption.order_index",
    )