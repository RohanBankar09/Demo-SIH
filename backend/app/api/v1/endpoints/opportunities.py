from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.industry import IndustryProfile
from app.models.opportunity import Opportunity
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse

router = APIRouter(
    prefix="/opportunities",
    tags=["Opportunities"],
)


@router.get(
    "/",
    response_model=list[OpportunityResponse],
)
def list_opportunities(
    db: Session = Depends(get_db),
):
    return (
        db.query(Opportunity)
        .filter(Opportunity.is_active.is_(True))
        .order_by(Opportunity.id.desc())
        .all()
    )


@router.post(
    "/",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity(
    data: OpportunityCreate,
    db: Session = Depends(get_db),
):
    industry_id = data.industry_id

    if not industry_id:
        # Fallback to first existing industry profile
        first_industry = db.query(IndustryProfile).first()
        if first_industry:
            industry_id = first_industry.id
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No Industry / Company profile found to associate this opportunity",
            )

    opp = Opportunity(
        industry_id=industry_id,
        title=data.title,
        opportunity_type=data.opportunity_type,
        description=data.description,
        location=data.location,
        work_mode=data.work_mode,
        duration=data.duration,
        stipend=data.stipend,
        experience_required=data.experience_required,
        eligibility=data.eligibility,
        is_active=True,
    )

    db.add(opp)
    db.commit()
    db.refresh(opp)

    return opp
