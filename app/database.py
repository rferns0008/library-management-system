import os
import logging
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

# -------------------------------------------------------------------
# Logging (MUST be defined before use)
# -------------------------------------------------------------------
logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
# Load environment variables
# -------------------------------------------------------------------
load_dotenv(override=True)


def get_database_url() -> str:
    """
    Returns the database URL with correct priority.

    Priority:
    1. TEST_DATABASE_URL when running pytest
    2. DATABASE_URL otherwise
    """
    if os.getenv("PYTEST_CURRENT_TEST"):
        db_url = os.getenv("TEST_DATABASE_URL")
    else:
        db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise RuntimeError("DATABASE_URL / TEST_DATABASE_URL is not set")

    logger.info("Using database URL: %s", db_url)

    return db_url


# -------------------------------------------------------------------
# SQLAlchemy async setup
# -------------------------------------------------------------------
DATABASE_URL = get_database_url()

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,      # ⭐ checks if connection is alive
    pool_recycle=1800,       # ♻️ refresh connections every 30 mins
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
