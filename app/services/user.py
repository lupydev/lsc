from uuid import UUID
from pydantic import EmailStr
from sqlmodel import select
from ..core.db import SessionDep
from ..core.security import get_password_hash, verify_password
from ..models import User
from ..schemas import UserCreate, UserUpdate
from ..api.deps import CurrentUser
from fastapi import HTTPException, status


async def create_user(
    user_create: UserCreate,
    db: SessionDep,
) -> User:
    email = await db.exec(select(User).where(User.email == user_create.email))
    email = email.first()

    if email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Un usuario ya se registró con el email: {user_create.email}, por favor ingresa otro correo para realizar el registro.",
        )
    user_create.password = get_password_hash(user_create.password)

    new_user = User(**user_create.model_dump())

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_email(
    email: EmailStr,
    db: SessionDep,
):
    user = await db.exec(select(User).where(User.email == email))

    return user.one()


async def get_user_by_id(
    id: UUID,
    db: SessionDep,
):
    user = await db.exec(select(User).where(User.id == id))
    return user.first()


async def authenticate(
    db: SessionDep,
    email: EmailStr,
    password: str,
) -> User | None:
    user = await get_user_by_email(db=db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay ningún usuario registrado con el correo: {email}",
        )
    if not verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta",
        )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def validate_user(
    id: UUID,
    current_user: CurrentUser,
    db: SessionDep,
):

    user = await db.exec(select(User).where(User.id == current_user.id))
    user = user.one()

    if user.id != id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes los permisos para realizar esta acción",
        )
    return user


async def user_update(
    id: UUID,
    user_update: UserUpdate,
    current_user: CurrentUser,
    db: SessionDep,
):
    user = await validate_user(id=id, current_user=current_user, db=db)

    user_data = user_update.model_dump(exclude_unset=True)

    user.sqlmodel_update(user_data)

    await db.commit()
    await db.refresh(user)

    return user


async def logical_delete(
    id: UUID,
    current_user: CurrentUser,
    db: SessionDep,
):
    user = await validate_user(id, current_user, db)
    user.is_active = False

    await db.commit()
    await db.refresh(user)
    return HTTPException(
        status_code=status.HTTP_204_NO_CONTENT,
        detail=f"El usuario: {user.name} ha sido eliminado",
    )
