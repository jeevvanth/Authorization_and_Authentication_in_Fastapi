from abc import abstractmethod,ABC
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schema import UserCreate,UserRead,Token
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer


class IUserInterface(ABC):

    @abstractmethod
    async def user_registration(self,db:AsyncSession,user_data:UserCreate)->UserRead:
        pass

    @abstractmethod
    async def login_access(self,db:AsyncSession,form_data:OAuth2PasswordRequestForm)->Token:
        pass

    
