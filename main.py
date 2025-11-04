from fastapi import FastAPI,Depends,HTTPException,status
from repository import UserRepository
from service import UserService
from schema import UserRead,UserCreate,Token
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from uvicorn import run
from password_func import create_access_token,get_current_user
from model import User
from jose import JWTError, jwt


app=FastAPI(title="Basic Reg and login with Authentication")


user_service=UserService(UserRepository())
user_repo=UserRepository()

@app.post("/Register",response_model=UserRead)
async def registeration(user_data:UserCreate,db:AsyncSession=Depends(get_db)):
    existing_user=await user_repo.get_user_by_email(db=db,email=user_data.email)
    if existing_user:
        raise HTTPException(status_code=400,detail="User already exist")
    try:
        user=await user_service.user_registration(db=db,user_data=user_data)
        return user

    except Exception as ex:
        raise HTTPException(status_code=400,detail=str(ex))

@app.post("/token",response_model=Token)
async def login_access_token(form_data:OAuth2PasswordRequestForm=Depends(),db:AsyncSession=Depends(get_db)):
    try:
        user_result=await user_service.login_access(db,form_data)
        access_token= await create_access_token({"sub":user_result.name, "email":user_result.email})
        return {"access_token":access_token,"token_type":"Bearer"}
    except Exception as ex:
        raise HTTPException(status_code=400,detail=str(ex))
    
@app.get("/current_user",response_model=UserRead)
async def get_user(current_user:User=Depends(get_current_user)):
    try:
        return current_user
    except Exception as ex:
        raise HTTPException(status_code=400,detail=str(ex))
    

    






if __name__=="__main__":
    run(
        "main:app",
        host="127.0.0.1",
        port=8001,
        reload=False
    )



