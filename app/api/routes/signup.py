from fastapi import APIRouter, status
from app.core.db import SessionDep
from app.schemas import NewUserResponse, UserCreate
from app.services.user import create_user

router = APIRouter()


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=NewUserResponse,
)
async def signup(
    new_uer: UserCreate,
    db: SessionDep,
):
    return await create_user(new_uer, db)
