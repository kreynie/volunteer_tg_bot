from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, create_async_engine
from src.config import settings

engine = create_async_engine(
    url=settings.db.url,
    echo=settings.db.echo,
)
session_maker = async_sessionmaker(engine)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
