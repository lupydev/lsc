from sqlmodel import Field
from .abstract import Abstract
from pydantic import EmailStr


class User(Abstract, table=True):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        index=True,
    )
    surname: str | None = Field(
        default=None,
        min_length=2,
        max_length=50,
        index=True,
    )
    email: EmailStr = Field(
        unique=True,
        index=True,
    )
    password: str = Field(min_length=6)
    superuser: bool = Field(default=True)
