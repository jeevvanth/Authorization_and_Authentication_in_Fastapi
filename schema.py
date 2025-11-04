from pydantic import BaseModel,EmailStr,constr
from typing import Optional

class UserCreate(BaseModel):
    email:EmailStr
    password:str
    name:str 

class UserRead(BaseModel):
    id:int
    email:EmailStr
    password:str
    name:str

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token:str
    token_type:str

