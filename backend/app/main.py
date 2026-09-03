from fastapi import FastAPI

from app.api.v1.endpoints.assessments import router as assessment_router
from app.api.v1.endpoints.attempts import router as attempt_router
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.opportunities import router as opportunity_router
from app.api.v1.endpoints.questions import router as question_router
from app.api.v1.endpoints.student import router as student_router
from app.core.database import engine
from app.models.base import Base
import app.models  # Ensure all models are registered

# Create newly registered tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PIXIE API",
    description="Academia–Industry Collaboration Platform",
    version="0.1.0",
)

app.include_router(
    auth_router,
    prefix="/api/v1",
)

app.include_router(
    student_router,
    prefix="/api/v1",
)

app.include_router(
    assessment_router,
    prefix="/api/v1",
)

app.include_router(
    question_router,
    prefix="/api/v1",
)

app.include_router(
    attempt_router,
    prefix="/api/v1",
)

app.include_router(
    opportunity_router,
    prefix="/api/v1",
)


@app.get("/")
def root():
    return {
        "message": "Welcome to PIXIE",
        "status": "running",
        "version": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "PIXIE API",
    }