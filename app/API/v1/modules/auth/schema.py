from pydantic import BaseModel
from ..users.schema import UserItem


class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "javier@foreach.cl",
                "password": "123",
            }
        }


class RecoverPasswordSchema(BaseModel):
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "email": "test@test.cl",
            }
        }


class PasswordChangeSchema(BaseModel):
    new_pass: str
    recovery_token: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "new_pass": "1234567890",
                "recovery_token": "asdhuashdujasd78as6f78as6d78ya7sdasd",
            }
        }


class ChangePasswordSchema(BaseModel):
    new_pass: str
    current_pass: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "current_pass": "1234567890",
                "new_pass": "1234567890",
            }
        }


class RecoveryTokenSchema(BaseModel):
    recovery_token: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "recovery_token": "3452fsdfsd8f7sd89f7sd89fusdfsdfse",
            }
        }


class MeResponseSchema(UserItem):
    class Config:
        orm_mode = True


class LoginUser(BaseModel):
    accessToken: str
    refreshToken: str
    user: UserItem
