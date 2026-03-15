import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# 1. Grab the URL from docker-compose, and format it for the async driver
raw_url = os.getenv("DATABASE_URL", "postgresql://ai_user:ai_password@db:5432/ai_gateway_db")
DATABASE_URL = raw_url.replace("postgresql://", "postgresql+asyncpg://")

# 2. Create the Async Engine
engine = create_async_engine(DATABASE_URL, echo=False)

# 3. Create a session factory
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# 4. Base class for our tables
Base = declarative_base()

# 5. FastAPI Dependency for getting a DB session per request
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session