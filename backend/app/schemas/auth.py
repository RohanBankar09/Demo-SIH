from pydantic import BaseModel, EmailStr, Field


class StudentRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    college_name: str | None = Field(default=None, max_length=200)
    degree: str | None = Field(default=None, max_length=100)
    branch: str | None = Field(default=None, max_length=100)
    graduation_year: int | None = None
    career_goal: str | None = Field(default=None, max_length=150)


class CompanyRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    company_name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=20)
    industry: str | None = Field(default=None, max_length=100)
    website: str | None = Field(default=None, max_length=300)
    contact_person: str | None = Field(default=None, max_length=150)
    location: str | None = Field(default=None, max_length=200)


class InstitutionRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    institution_name: str = Field(min_length=2, max_length=200)
    phone: str | None = Field(default=None, max_length=20)
    institution_type: str | None = Field(default=None, max_length=100)
    location: str | None = Field(default=None, max_length=200)
    contact_person: str | None = Field(default=None, max_length=150)
    website: str | None = Field(default=None, max_length=300)


class AcademicianRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    full_name: str = Field(min_length=2, max_length=150)
    phone: str | None = Field(default=None, max_length=20)
    institution_name: str | None = Field(default=None, max_length=200)
    department: str | None = Field(default=None, max_length=100)
    designation: str | None = Field(default=None, max_length=100)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=1,
        max_length=72,
    )


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    is_verified: bool

    model_config = {
        "from_attributes": True,
    }