import sys
from fastapi import APIRouter, status, Response
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from ..users.model import usersTable, rolesTable
from .schema import LoginSchema
from .....config.db import conn
from ...helpers.security import verify_password, create_access_token, create_refresh_token
from ...constans.security import IS_PRODUCTION


router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login_user(body: LoginSchema, response: Response):
    try:
        stmt = (
            select(
                usersTable,                      
                rolesTable.c.id.label('roles_table_id'), 
                rolesTable.c.name.label('roles_table_name')
            )
            .select_from(usersTable.join(rolesTable, usersTable.c.role_id == rolesTable.c.id))
            .where(usersTable.c.email == body.email)
        )

        found_user = conn.execute(stmt).first()

        user_data = {column: found_user[column] for column in usersTable.columns.keys()}

        role_data = {
            'name': found_user['roles_table_name']
        }

        del user_data['password']
        del user_data['created_at']
        del user_data['updated_at']
        user_data['role'] = role_data


        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuario no está registrado",
            )
        
        match_password = verify_password(body.password, found_user.password)
        if not match_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas"
            )
        
        user_obj = {
            "accessToken": create_access_token(found_user.id),
            "refreshToken": create_refresh_token(found_user.id),
            "user": user_data
        }
        
        print(user_obj)
        response = JSONResponse(content=user_obj)
        response.set_cookie(key='accessToken', value=user_obj['accessToken'], httponly=IS_PRODUCTION, secure=IS_PRODUCTION)
        response.set_cookie(key='refreshToken', value=user_obj['refreshToken'], httponly=IS_PRODUCTION, secure=IS_PRODUCTION)
        return response
    
    except Exception as err:
        print("Error in line:", sys.exc_info()[-1].tb_lineno)
        print("Error message : {0}".format(err))
        if hasattr( err, "detail"):
            
            raise HTTPException(
                status_code=400,
                detail= err.detail,
            )
        else:
            raise HTTPException(400, format(err))