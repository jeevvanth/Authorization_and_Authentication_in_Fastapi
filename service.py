from sqlalchemy.ext.asyncio import AsyncSession
from interface import IUserInterface
from repository import UserRepository
from schema import UserCreate
from model import User
from typing import Optional
from fastapi.security import OAuth2PasswordRequestForm


class UserService(IUserInterface):
    def __init__(self,repo:UserRepository):
        self.repo=repo

    async def user_registration(self,db:AsyncSession,user_data:UserCreate)->Optional[User]:
        result= await self.repo.user_create(db=db,user_data=user_data)
        return result
    
    async def login_access(self, db:AsyncSession, form_data:OAuth2PasswordRequestForm)->Optional[User]:
        # return await super().login_access(db, form_data)
        result=await self.repo.authenticate_user(db,form_data.username,form_data.password)
        return result
    
    
    