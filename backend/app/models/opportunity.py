from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Opportunity(Base):
    __tablename__ = "opportunities"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    industry_id: Mapped[int] = mapped_column(
        ForeignKey("industry_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
        index=True,
    )

    opportunity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    location: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    work_mode: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True,
    )

    duration: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    stipend: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    experience_required: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    eligibility: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    application_deadline: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )