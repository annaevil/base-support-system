from sqlalchemy.orm import (
    declarative_base,
    sessionmaker,
)
from typing import AsyncGenerator
from sqlalchemy import MetaData

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from database.settings import db_settings

DB_URL = db_settings.db_url

print(f'Database connect on {DB_URL}')

Base = declarative_base()
engine = create_async_engine(DB_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

metadata = MetaData()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
