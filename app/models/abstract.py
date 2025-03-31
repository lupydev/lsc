from datetime import datetime
import sqlalchemy
from sqlmodel import Field, SQLModel
from uuid import UUID, uuid4
from ..services import timing


class Abstract(SQLModel):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
    )
    created_at: datetime = Field(
        default_factory=timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sqlalchemy.func.now()},
    )
    updated_at: datetime = Field(
        default_factory=timing.get_utc_now,
        sa_type=sqlalchemy.DateTime(timezone=True),
        sa_column_kwargs={
            "onupdate": sqlalchemy.func.now(),
            "server_default": sqlalchemy.func.now(),
        },
    )
