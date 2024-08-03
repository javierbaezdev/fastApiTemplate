from pydantic import BaseModel, Field
from typing import Optional


class RoleItem(BaseModel):
    id: int
    name: str


class UserBase(BaseModel):
    full_name: str = Field(alias="fullName")
    email: str
    phone: str


class UserAutoRegister(UserBase):
    password: str
    confirm_password: str = Field(alias="confirmPassword")
    accept_terms: bool = Field(alias="acceptTerms")

    class Config:
        schema_extra = {
            "example": {
                "full_name": "javier baez",
                "email": "javier@foreach.cl",
                "phone": "123456789",
                "password": "123",
                "confirm_password": "123",
                "accept_terms": True,
            }
        }
    
class UserItem(UserBase):
    id: int
    role_id: Optional[int] = Field(alias="roleId")
    role: RoleItem


