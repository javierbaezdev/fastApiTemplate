from pydantic import BaseModel, Field
from typing import Optional


class RoleItem(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        json_encoders = {
            str: lambda v: v
        }


class UserBase(BaseModel):
    full_name: str = Field(alias="fullName")
    email: str
    phone: str

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {
            str: lambda v: v
        }


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


    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        json_encoders = {
            str: lambda v: v
        }