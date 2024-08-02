from fastapi import APIRouter
from fastapi.exceptions import HTTPException


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_user():
    try:
        return {"message": "login"}
    except exc.SQLAlchemyError as err:
        raise HTTPException(404, format(err))