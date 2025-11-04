from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker,declarative_base

Database_url= "mysql+aiomysql://root:jeevanth11@127.0.0.1:3306/user_db"


engin=create_async_engine(Database_url,echo=True)
AsyncSessionLocal=sessionmaker(bind=engin,class_=AsyncSession,expire_on_commit=False)
Base=declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
