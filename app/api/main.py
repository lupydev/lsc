from ..api.routes import auth, signup
from fastapi import APIRouter

api_router = APIRouter()


api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"],
)

api_router.include_router(
    signup.router,
    prefix="/super/signup",
    tags=["User"],
)
