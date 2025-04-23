from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ...core.db import SessionDep
from ...core.security import create_access_token, create_refresh_token
from ...schemas.token import Token
from ...services.token import token_refresh
from ...services.user import authenticate
from ...core.config import settings

router = APIRouter()


@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=Token,
)
async def login_acces_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: SessionDep,
):
    user = await authenticate(
        db,
        form_data.username,  #! se utiliza username ya que aqui es donde se ingresa el email en el form
        form_data.password,
    )
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No eres super usuario, no puedes iniciar sesión.",
        )

    return Token(
        access_token=create_access_token(
            user.id,
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            pioneer=user.pioneer.value,
        ),
        refresh_token=create_refresh_token(
            user.id,
            expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        ),
        pioneer=user.pioneer,
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_token: str,
    db: SessionDep,
):
    return await token_refresh(refresh_token, db)
