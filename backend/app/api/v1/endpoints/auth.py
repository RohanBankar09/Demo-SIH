from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.models.academician import AcademicianProfile
from app.models.company import CompanyProfile
from app.models.institution import InstitutionProfile
from app.models.student import StudentProfile
from app.models.user import User
from app.schemas.auth import (
    AcademicianRegister,
    CompanyRegister,
    InstitutionRegister,
    LoginRequest,
    StudentRegister,
    TokenResponse,
    UserResponse,
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

bearer_scheme = HTTPBearer()


@router.post(
    "/register/student",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_student(
    data: StudentRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="student",
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    db.flush()

    student = StudentProfile(
        user_id=user.id,
        full_name=data.full_name,
        phone=data.phone,
        college_name=data.college_name,
        degree=data.degree,
        branch=data.branch,
        graduation_year=data.graduation_year,
        career_goal=data.career_goal,
    )

    db.add(student)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/register/company",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_company(
    data: CompanyRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="company",
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    db.flush()

    company = CompanyProfile(
        user_id=user.id,
        company_name=data.company_name,
        phone=data.phone,
        industry=data.industry,
        website=data.website,
        contact_person=data.contact_person,
        location=data.location,
    )

    db.add(company)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/register/institution",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_institution(
    data: InstitutionRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="institution",
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    db.flush()

    institution = InstitutionProfile(
        user_id=user.id,
        institution_name=data.institution_name,
        phone=data.phone,
        institution_type=data.institution_type,
        location=data.location,
        contact_person=data.contact_person,
        website=data.website,
    )

    db.add(institution)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/register/academician",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register_academician(
    data: AcademicianRegister,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        role="academician",
        is_active=True,
        is_verified=False,
    )

    db.add(user)
    db.flush()

    academician = AcademicianProfile(
        user_id=user.id,
        full_name=data.full_name,
        phone=data.phone,
        institution_name=data.institution_name,
        department=data.department,
        designation=data.designation,
    )

    db.add(academician)
    db.commit()
    db.refresh(user)

    return user


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not verify_password(
        data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=403,
            detail="User account is inactive",
        )

    access_token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if not user_id:
            raise ValueError("Missing user ID")

        user = db.get(User, int(user_id))

    except (ValueError, TypeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return user