from datetime import datetime
from uuid import UUID
from sqlmodel import SQLModel, Field
from pydantic import EmailStr, field_validator
from ..utils.validators import validate_names


class UserLogin(SQLModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=255,
    )


class UserCreate(UserLogin):
    name: str = Field(
        min_length=2,
        max_length=40,
    )
    surname: str = Field(
        min_length=2,
        max_length=40,
    )

    @field_validator("name", "surname")
    def valitate_name_surname(cls, value):
        return validate_names(value)


class UserResponse(SQLModel):
    id: UUID
    name: str
    surname: str
    email: EmailStr


class NewUserResponse(UserResponse):
    created_at: datetime


class UserUpdate(SQLModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=40,
    )
    surname: str | None = Field(
        default=None,
        min_length=2,
        max_length=40,
    )
    email: EmailStr | None = None

    @field_validator("name", "surname")
    def valitate_name_surname(cls, value):
        return validate_names(value)


class PasswordUpdate(SQLModel):
    current_password: str = Field(
        min_length=8,
        max_length=255,
    )
    new_password: str = Field(
        min_length=8,
        max_length=255,
    )
