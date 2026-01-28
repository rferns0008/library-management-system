import os
from dotenv import load_dotenv

# --------------------------------------------------
# CRITICAL: FORCE TEST DB BEFORE APP IMPORTS
# --------------------------------------------------
load_dotenv(override=True)

test_db = os.getenv("TEST_DATABASE_URL")
if not test_db:
    raise RuntimeError("TEST_DATABASE_URL missing")

os.environ["PYTEST_RUNNING"] = "1"
os.environ["DATABASE_URL"] = test_db

# --------------------------------------------------
# NOW SAFE TO IMPORT APP
# --------------------------------------------------

import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app.main import app
from app.database import Base
from app.dependencies import get_db

# --------------------------------------------------
# Async engine for tests
# --------------------------------------------------

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool,
)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# --------------------------------------------------
# Fresh schema at test start
# --------------------------------------------------

@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield

# --------------------------------------------------
# Persistent DB session per request
# --------------------------------------------------

@pytest_asyncio.fixture
async def client():
    async def override_get_db():
        session = AsyncSessionLocal()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()