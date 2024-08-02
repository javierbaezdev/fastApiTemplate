from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from .model import usersTable
from .....config.db import conn

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/all")
async def get_users():
    return conn.execute(usersTable.select()).fetchall()