from sqlalchemy.orm import Session
from ..models import Loan, Book
 
MAX_BORROW_LIMIT = 5
 
def validate_member_can_borrow(db: Session, member_id: int):
    active_loans = db.query(Loan).filter(
        Loan.member_id == member_id,
        Loan.return_date == None
    ).count()
 
    if active_loans >= MAX_BORROW_LIMIT:
        raise ValueError("Member cannot borrow more than 5 books")
 
def validate_book_not_loaned(db: Session, book_id: int):
    active_loan = db.query(Loan).filter(
        Loan.book_id == book_id,
        Loan.return_date == None
    ).first()
 
    if active_loan:
        raise ValueError("Cannot delete a loaned-out book")