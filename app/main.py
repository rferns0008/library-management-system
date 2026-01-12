from fastapi import FastAPI

from app.routers import books, members, loans
from app.database import engine, Base

app = FastAPI(
    title="Library Management System API",
    version="1.0.0",
)

# --------------------------------------------------
# Include routers
# --------------------------------------------------

app.include_router(books.router)
app.include_router(members.router)
app.include_router(loans.router)


# --------------------------------------------------
# Startup event: create tables if they don't exist
# --------------------------------------------------

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# --------------------------------------------------
# Optional health check (useful for debugging)
# --------------------------------------------------

@app.get("/health", tags=["Health"])
def health():
    return {"status": "ok"}