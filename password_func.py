from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Optional
from datetime import datetime,timedelta
from fastapi import Depends,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from model import User
from fastapi.security import OAuth2PasswordBearer

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth_scheme=OAuth2PasswordBearer(tokenUrl="/token")

async def get_password_hash(password:str)->str:
    return await pwd_context.hash(password)

async def verify_password(plan_password:str,hashed_password:str)->bool:
    return await pwd_context.verify(plan_password,hashed_password)


async def create_access_token(data: dict, expire_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token:str=Depends(oauth_scheme),db:AsyncSession=Depends(get_db))->Optional[User]:
    credential_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate the credential",
        headers={"WWW-Authenticate":"Bearer"}
    )
    print("token:",token)
    # try:
        
    payload= jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
    print("token_payload:",payload)
    user_email:str=payload.get("email")
    print("user_id:",user_email)
    if user_email is None:
        raise credential_exception

    # except JWTError:
    #     raise credential_exception
    user=await db.execute(select(User).where(User.email==user_email))
    user_detail= user.scalar_one_or_none()
    print("user:",user_detail)

    if not user:
        raise credential_exception
    
    return {"id":user_detail.id,"email":user_detail.email,"password":user_detail.hashed_password,"name":user_detail.name}
