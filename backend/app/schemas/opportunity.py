from datetime import datetime

from pydantic import BaseModel, Field


class OpportunityBase(BaseModel):
    title: str = Field(min_length=2, max_length=200)
    opportunity_type: str = Field(default="Internship", max_length=50)
    description: str = Field(min_length=5)
    location: str | None = Field(default="Remote", max_length=200)
    work_mode: str | None = Field(default="Remote", max_length=30)
    duration: str | None = Field(default="3 Months", max_length=100)
    stipend: int | None = Field(default=25000)
    experience_required: str | None = Field(default="Fresher", max_length=100)
    eligibility: str | None = Field(default="B.Tech / B.Sc in Computer Science or related", max_length=500)


class OpportunityCreate(OpportunityBase):
    industry_id: int | None = None


class OpportunityResponse(OpportunityBase):
    id: int
    industry_id: int
    is_active: bool
    created_at: datetime | None = None

    model_config = {
        "from_attributes": True,
    }
