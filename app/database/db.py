from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@db:5432/appDB"


engine = create_async_engine(DATABASE_URL, future=True, echo=True)

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def init_db():
    """
    Initialize the database by creating all tables defined in the metadata.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@asynccontextmanager
async def get_db_session() -> AsyncSession:
    """
    Asynchronous context manager for obtaining a database session.
    """
    async with SessionLocal() as session:
        yield session
