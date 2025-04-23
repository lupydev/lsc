from sqlmodel import Field
from .abstract import Abstract
from .enum import Territory
from uuid import UUID


class Location(Abstract, table=True):
    territory: Territory
    description: str = Field(
        min_length=2,
        max_length=150,
    )
    latitude: float = Field(
        ge=-90,
        le=90,
    )
    longitude: float = Field(
        ge=-180,
        le=180,
    )
    place_id: str = Field(
        max_length=100,
    )
    user_id: UUID = Field(foreign_key="user.id")
