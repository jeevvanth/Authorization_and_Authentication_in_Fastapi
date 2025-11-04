from sqlalchemy import Column,Integer,String,DateTime
from database import Base
from datetime import datetime

class User(Base):
    __tablename__="users_details"

    id=Column(Integer,primary_key=True,index=True,autoincrement=True)
    name=Column(String(100),nullable=True)
    email=Column(String(100),unique=True,nullable=False)
    hashed_password=Column(String(200),nullable=False)
    create_at=Column(DateTime,default=datetime.utcnow)
