from sqlalchemy.ext.asyncio import AsyncSession
from schema import UserCreate,Token
from password_func import get_password_hash,verify_password,create_access_token
from model import User
from sqlalchemy.future import select
from typing import Optional
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm


class UserRepository:

    async def get_user_by_email(self,db:AsyncSession,email:str)->Optional[User]:
        user=await db.execute(select(User).where(User.email==email))
        return user.scalar_one_or_none()
    
    async def get_user_by_id(self,db:AsyncSession,id:int)->User:
        user=await db.execute(select(User).where(User.id==id))
        return user.scalar_one_or_none()

        
    
    async def user_create(self,db:AsyncSession,user_data:UserCreate)->User:
        password:str=await get_password_hash(user_data.password)
        user=User(email=user_data.email,hashed_password=password,name=user_data.name)
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
    
    async def authenticate_user(self,db:AsyncSession,email:str,password:str)->User:
        user= await self.get_user_by_email(db=db,email=email)
        print("password:",password)
        print("password:",user.hashed_password)

        if not user:
            raise HTTPException(status_code=400,detail="user not found")
        
        if not  verify_password(plan_password=password,hashed_password=user.hashed_password):
            raise HTTPException(status_code=400,detail="wrong password")
        
        return user



        
    
    
        
