from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..dependencies import get_db
from ..models import Book as BookModel
from ..schemas import BookCreate, Book
from ..crud import delete_book

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=Book)
async def create_book(book: BookCreate, db: AsyncSession = Depends(get_db)):
    obj = BookModel(**book.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[Book])
async def list_books(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(BookModel))
    return res.scalars().all()


# ✅ FIX: required by test_get_book_by_id
@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(BookModel).where(BookModel.id == book_id)
    )
    book = res.scalars().first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.delete("/{book_id}")
async def delete_book_handler(book_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_book(db, book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"status": "deleted"}