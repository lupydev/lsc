from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import init_db
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para el sistema de LSC",
    version="0.0.1",
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
