from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import date

from ..dependencies import get_db
from ..models import Loan as LoanModel, Book as BookModel, Member as MemberModel
from ..schemas import LoanCreate, Loan

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.post("/", response_model=Loan)
async def create_loan(loan: LoanCreate, db: AsyncSession = Depends(get_db)):
    # Validate book
    book = await db.get(BookModel, loan.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    # Validate member
    member = await db.get(MemberModel, loan.member_id)
    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    # ✅ FIX: enforce borrowing limit (max 5)
    result = await db.execute(
        select(func.count())
        .select_from(LoanModel)
        .where(
            LoanModel.member_id == loan.member_id,
            LoanModel.return_date.is_(None)
        )
    )
    active_loans = result.scalar()

    if active_loans >= 5:
        raise HTTPException(
            status_code=400,
            detail="Member cannot borrow more than 5 books"
        )

    obj = LoanModel(
        book_id=loan.book_id,
        member_id=loan.member_id,
        loan_date=date.today()
    )
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.post("/{loan_id}/return", response_model=Loan)
async def return_loan(loan_id: int, db: AsyncSession = Depends(get_db)):
    loan = await db.get(LoanModel, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    loan.return_date = date.today()
    await db.commit()
    await db.refresh(loan)
    return loan