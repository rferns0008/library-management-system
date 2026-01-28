import os
import logging
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------
load_dotenv(override=False)

def get_database_url() -> str:
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL not set")
    return db_url

# -------------------------------------------------------------------
# SQLAlchemy async setup
# -------------------------------------------------------------------
DATABASE_URL = get_database_url()

# 🚨 SAFETY GUARD — tests must NEVER use production DB
if os.getenv("PYTEST_RUNNING") == "1":
    if "library_db_test" not in DATABASE_URL:
        raise RuntimeError("🚨 TESTS ARE POINTING TO PRODUCTION DATABASE!")

logger.info("Using database URL: %s", DATABASE_URL)

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_recycle=1800,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session