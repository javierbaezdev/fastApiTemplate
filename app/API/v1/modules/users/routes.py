import sys
from typing import List
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.param_functions import Depends
from sqlalchemy.orm.session import Session
from app.database.main import get_database

from ...middlewares.verify_cookie import verify_cookie
from ...services.security import get_password_hash
from app.API.v1.modules.users.schema import UserAutoRegister, UserItem
from app.API.v1.modules.users.model import User, AcceptedTerms


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/auto-register")
def create_user(body: UserAutoRegister, db: Session = Depends(get_database)):
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
        current_user = db.query(User).filter(User.email == body.email).first()
        if current_user:
            raise HTTPException(
                status_code=400,
                detail="El email ya esta registrado",
            )
       
        hashed_password = get_password_hash(body.password)
        user_data = body.dict()
        del user_data['confirm_password']
        del user_data['accept_terms']
        user_data['password'] = hashed_password
        user_data['role_id'] = 1 # Default role is CLIENTS

        new_user = User(**user_data)
        db.add(new_user)
        db.commit()
        db.flush(User)

        user_id = new_user.id
        accepted_terms = AcceptedTerms(user_id=user_id, description='ok')
        db.add(accepted_terms)
        db.commit()
        db.flush(AcceptedTerms)

        del user_data['password']
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
        


@router.get("/get-all-users", dependencies=[Depends(verify_cookie)])
def get_all_users(request: Request, db: Session = Depends(get_database)):
    try:
        user_id_auth = request.user_id_auth
        print('user_id_auth =>>>>>>>>>>>>>>>>>>>>>', user_id_auth)
        return db.query(User).all()
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

