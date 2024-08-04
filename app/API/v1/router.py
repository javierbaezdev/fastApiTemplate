from fastapi import APIRouter
from .modules.users import user_router
from .modules.auth import auth_router

v1_router = APIRouter()

v1_router.include_router(user_router)
v1_router.include_router(auth_router)
