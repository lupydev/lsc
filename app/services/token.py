from datetime import datetime
from fastapi import HTTPException, status
from jose import JWTError
from ..core.db import SessionDep
from ..core.config import settings
from ..core.security import create_access_token
from ..schemas.token import Token, TokenPayload
from ..services.user import get_user_by_id


def token_refresh(
    refresh_token: str,
    db: SessionDep,
):
    try:
        # Decode token even if expired
        payload = JWTError.decode(
            refresh_token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"verify_exp": False},  # Important: Don't reject expired tokens yet
        )
        token_data = TokenPayload(**payload)

        user = get_user_by_id(token_data.sub, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no encontrado.",
            )

        # Check user activity in last 8 days
        days_since_login = (datetime.now() - user.last_login).days
        if days_since_login <= 8:
            # User was active - generate new tokens
            access_token = create_access_token(
                user.id,
                settings.ACCESS_TOKEN_EXPIRE_MINUTES,
                user.pioneer.value,
            )

            new_refresh_token = create_access_token(
                user.id,
                minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES,
                pioneer=user.pioneer.value,
            )

            return Token(
                access_token=access_token,
                refresh_token=new_refresh_token,
                pioneer=user.pioneer,
            )
        else:
            # Inactive user - force logout
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="La sesión expiro por inactividad en la aplicación.",
            )

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token invalido."
        )
