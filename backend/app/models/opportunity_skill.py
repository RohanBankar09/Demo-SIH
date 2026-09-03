from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class OpportunitySkill(Base):
    __tablename__ = "opportunity_skills"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    opportunity_id: Mapped[int] = mapped_column(
        ForeignKey("opportunities.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skills.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    required_proficiency: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    is_mandatory: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )