from datetime import date
from typing import Optional, List

from pydantic import BaseModel, EmailStr
from sqlalchemy import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Book as BookModel, Member as MemberModel, Loan as LoanModel

# ======================================================
# ==================== SCHEMAS =========================
# ======================================================

# ---- Books ----
class BookBase(BaseModel):
    title: str
    author: str
    isbn: str
    published_date: Optional[date] = None

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    class Config:
        from_attributes = True


# ---- Members ----
class MemberBase(BaseModel):
    name: str
    email: EmailStr
    membership_date: Optional[date] = None

class MemberCreate(MemberBase):
    pass

class Member(MemberBase):
    id: int
    class Config:
        from_attributes = True


# ---- Loans ----
class LoanCreate(BaseModel):
    book_id: int
    member_id: int

class Loan(BaseModel):
    id: int
    book_id: int
    member_id: int
    loan_date: date
    return_date: Optional[date]

    class Config:
        from_attributes = True


# ======================================================
# ===================== CRUD ===========================
# ======================================================

# ------------------ BOOKS ------------------

async def create_book(db: AsyncSession, book: BookCreate) -> BookModel:
    db_book = BookModel(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book


async def get_books(db: AsyncSession) -> List[BookModel]:
    result = await db.execute(select(BookModel))
    return result.scalars().all()


async def get_book(db: AsyncSession, book_id: int) -> Optional[BookModel]:
    result = await db.execute(
        select(BookModel).where(BookModel.id == book_id)
    )
    return result.scalar_one_or_none()


async def delete_book(db: AsyncSession, book_id: int) -> bool:
    result = await db.execute(
        delete(BookModel).where(BookModel.id == book_id)
    )
    await db.commit()
    return result.rowcount > 0


# ------------------ MEMBERS ------------------

async def create_member(db: AsyncSession, member: MemberCreate) -> MemberModel:
    db_member = MemberModel(**member.dict())
    db.add(db_member)
    await db.commit()
    await db.refresh(db_member)
    return db_member


async def get_members(db: AsyncSession) -> List[MemberModel]:
    result = await db.execute(select(MemberModel))
    return result.scalars().all()


async def delete_member(db: AsyncSession, member_id: int) -> bool:
    result = await db.execute(
        delete(MemberModel).where(MemberModel.id == member_id)
    )
    await db.commit()
    return result.rowcount > 0


# ------------------ LOANS ------------------

async def create_loan(db: AsyncSession, loan: LoanCreate) -> LoanModel:
    db_loan = LoanModel(**loan.dict())
    db.add(db_loan)
    await db.commit()
    await db.refresh(db_loan)
    return db_loan