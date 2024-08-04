import sys
from fastapi import APIRouter, security, status, Response
from fastapi.exceptions import HTTPException
from fastapi.params import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.params import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import exc
from sqlalchemy.orm import Session, joinedload
from starlette.requests import Request
from .....config import config
from app.database.main import get_database
from ...services.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    decodeRefreshJWT,
    create_recovery_token,
    get_password_hash,
    decodeRecoverJWT,
)
from ...middlewares.auth import JWTBearer, decodeJWT
from ..users.model import User
from .schema import (
    LoginSchema,
    MeResponseSchema,
    LoginUser,
    RecoverPasswordSchema,
    RecoveryTokenSchema,
    PasswordChangeSchema,
    ChangePasswordSchema,
)
""" from ...services.mail_service import send_recovery_password_mail """

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


def is_authenticated(auth_token):
    try:
        if decodeJWT(auth_token):
            return get_database
        else:
            return False

    except Exception as err:
        print("Error message {0}".format(err))


def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    return is_authenticated(auth.credentials)


@router.post("/login")
async def login_user(login_obj: LoginSchema, response: Response, db: Session = Depends(get_database)):
    try:
        found_user = db.query(User).options(joinedload(User.role)).filter(User.email == login_obj.email).first()


        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este usuario no está registrado",
            )
        
        match_password = verify_password(login_obj.password, found_user.password)
        if not match_password:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Credenciales incorrectas"
            )
        
        user_obj = {
            "accessToken": create_access_token(found_user.id),
            "refreshToken": create_refresh_token(found_user.id),
            "user": {
                "id": found_user.id,
                "fullName": found_user.full_name,
                "email": found_user.email,
                "phone": found_user.phone,
                "roleId": found_user.role_id,
                "role": {
                    "id": found_user.role.id,
                    "name": found_user.role.name
                }
            }
        }
        
        response = JSONResponse(content=user_obj)
        response.set_cookie(key='accessToken', value=user_obj['accessToken'], httponly=config.IS_PRODUCTION, secure=config.IS_PRODUCTION)
        response.set_cookie(key='refreshToken', value=user_obj['refreshToken'], httponly=config.IS_PRODUCTION, secure=config.IS_PRODUCTION)
        return response
    except exc.SQLAlchemyError as err:
        print('line error', sys.exc_info()[-1].tb_lineno)

        raise HTTPException(404, format(err))


@router.get("/me", response_model=MeResponseSchema, dependencies=[Depends(JWTBearer())])
async def get_logged_user(request: Request, db: Session = Depends(get_database)):
    try:
        user_id = int(request.user_id)

        current_user = db.query(User).filter(User.id == user_id).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin autorización"
            )
        return current_user

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(err.status_code, format(err.detail))
        else:
            raise HTTPException(404, format(err))


@router.post("/changepassword", dependencies=[Depends(JWTBearer())])
async def change_password_logged_user(
    body: ChangePasswordSchema, request: Request, db: Session = Depends(get_database)
):
    try:
        user_id = int(request.user_id)

        current_user = db.query(User).filter(User.id == user_id).first()

        if not current_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin autorización"
            )

        setattr(current_user, "password", get_password_hash(body.new_pass))

        db.add(current_user)
        db.commit()
        db.flush(current_user)

        return current_user

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(err.status_code, format(err.detail))
        else:
            raise HTTPException(404, format(err))


@router.post("/forgotpassword")
async def recover_password(
    body: RecoverPasswordSchema, db: Session = Depends(get_database)
):
    try:
        found_user = db.query(User).filter(User.email == body.email).first()
        if not found_user:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Este email no está registrado",
            )
        recovery_token = create_recovery_token(found_user.id)

        """ send_recovery_password_mail(
            found_user.email,
            found_user.name,
            recovery_token,
        ) """

        return JSONResponse(
            status_code=200,
            content={"message": "EMAIL_SENT"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


@router.post("/recoverpassword")
async def recovery_password(
    body: PasswordChangeSchema, db: Session = Depends(get_database)
):
    try:
        token = decodeRecoverJWT(body.recovery_token)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token Inválido"
            )

        user = db.query(User).filter(User.id == token["sub"]).first()

        setattr(user, "password", get_password_hash(body.new_pass))

        db.add(user)
        db.commit()
        db.flush(user)

        return JSONResponse(
            status_code=200,
            content={"message": "USER_UPDATED"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


@router.post("/check-recovery-token")
async def check_recovery_token(body: RecoveryTokenSchema):
    try:
        token = decodeRecoverJWT(body.recovery_token)

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Token Inválido"
            )

        return JSONResponse(
            status_code=200,
            content={"message": "TOKEN IS VALID"},
        )

    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))


@router.post("/changetoken", dependencies=[Depends(JWTBearer())])
async def change_token(request: Request, refresh_token: str):
    try:
        token = decodeRefreshJWT(refresh_token)
        user_id = request.user_id

        if not token:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Usuarios no coinciden"
            )

        if token["sub"] == user_id:
            access_token = create_access_token(token["sub"])
            return access_token

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Usuario sin autorización"
        )
    except Exception as err:
        print("Error message : {0}".format(err))
        if hasattr(err, "detail"):
            raise HTTPException(404, format(err.detail))
        else:
            raise HTTPException(404, format(err))
