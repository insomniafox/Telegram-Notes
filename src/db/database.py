from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import settings


DATABASE_URL = "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
    user=settings.POSTGRES_USER,
    password=settings.POSTGRES_PASSWORD,
    host=settings.POSTGRES_HOST,
    port=settings.POSTGRES_PORT,
    db=settings.POSTGRES_DB,
)

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)


async def get_sqlalchemy_session():
    SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    session = SessionLocal()
    try:
        yield session
    finally:
        await session.close()
