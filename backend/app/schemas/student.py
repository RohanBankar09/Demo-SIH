from pydantic import BaseModel, EmailStr, Field


class StudentProfileUpdate(BaseModel):
    full_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    phone: str | None = Field(
        default=None,
        max_length=20,
    )

    college_name: str | None = Field(
        default=None,
        max_length=200,
    )

    degree: str | None = Field(
        default=None,
        max_length=100,
    )

    branch: str | None = Field(
        default=None,
        max_length=100,
    )

    graduation_year: int | None = None

    career_goal: str | None = Field(
        default=None,
        max_length=150,
    )

    bio: str | None = Field(
        default=None,
        max_length=1000,
    )


class StudentProfileResponse(BaseModel):
    id: int
    user_id: int
    email: EmailStr
    full_name: str
    phone: str | None = None
    college_name: str | None = None
    degree: str | None = None
    branch: str | None = None
    graduation_year: int | None = None
    career_goal: str | None = None
    bio: str | None = None

    model_config = {
        "from_attributes": True,
    }