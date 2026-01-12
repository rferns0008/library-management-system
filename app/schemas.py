from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

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