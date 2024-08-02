from fastapi import APIRouter
from .modules.auth import auth_router
from .modules.users import users_router

v1_router = APIRouter()

v1_router.include_router(auth_router)
v1_router.include_router(users_router)
