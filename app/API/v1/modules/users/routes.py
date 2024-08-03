import sys
from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from .model import usersTable, acceptedTermsTable, rolesTable
from .schema import UserAutoRegister
from .....config.db import conn
from ...helpers.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/all")
async def get_users():
    return conn.execute(usersTable.select()).fetchall()


@router.post("/auto-register")
async def auto_register_user(body: UserAutoRegister):
    try:
        if (body.password != body.confirm_password):
            raise HTTPException(
                status_code=400,
                detail="las contraseñas no coinciden",
            )
        
        if not body.accept_terms:
            raise HTTPException(
                status_code=400,
                detail="Tienes que aceptar los términos y condiciones",
            )
        
        
        # validate email
        current_user = conn.execute(usersTable.select().where(usersTable.c.email == body.email)).first()
        if current_user:
            raise HTTPException(
                status_code=400,
                detail="El email ya esta registrado",
            )
       
        hashed_password = get_password_hash(body.password)
        new_user = {"full_name": body.full_name, "email": body.email, "phone": body.phone, "password": hashed_password, "role_id": 1} # Default role is CLIENTS
        
        result = conn.execute(usersTable.insert().values(new_user))

        user_id = result.lastrowid

        accepted_terms = {"user_id": user_id, "description": "ok"}
        conn.execute(acceptedTermsTable.insert().values(accepted_terms))
        
        stmt = (
            select(
                usersTable,                      
                rolesTable.c.id.label('roles_table_id'), 
                rolesTable.c.name.label('roles_table_name')
            )
            .select_from(usersTable.join(rolesTable, usersTable.c.role_id == rolesTable.c.id))
            .where(usersTable.c.id == user_id)
        )

        user_created = conn.execute(stmt).first()

        user_data = {column: user_created[column] for column in usersTable.columns.keys()}

        role_data = {
            'name': user_created['roles_table_name']
        }

        del user_data['password']
        user_data['role'] = role_data

        return user_data
            


        
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