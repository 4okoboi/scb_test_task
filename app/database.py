from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_async_engine(
    DATABASE_URL,
    future=True,
    execution_options={"isolation_level": "AUTOCOMMIT"},
)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    try:
        session: AsyncSession = async_session()
        yield session
    finally:
        await session.close()
        
class DAL:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
