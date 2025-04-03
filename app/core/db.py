from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core.config import settings
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker


engine = create_async_engine(
    settings.POSTGRES_URL,
    future=True,
    echo=True,  # Logger
)


async def init_db() -> None:
    async with engine.begin() as conn:
        # TODO: Aqui se agregan los modelos que se desean tener encuenta para crear las tablas en la base de datos

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
    async with async_session() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_session)]
