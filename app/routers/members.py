from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ..dependencies import get_db
from ..models import Member as MemberModel
from ..schemas import MemberCreate, Member
from ..crud import delete_member

router = APIRouter(prefix="/members", tags=["Members"])


@router.post("/", response_model=Member)
async def create_member(member: MemberCreate, db: AsyncSession = Depends(get_db)):
    obj = MemberModel(**member.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[Member])
async def list_members(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(MemberModel))
    return res.scalars().all()


@router.get("/{member_id}", response_model=Member)
async def get_member(member_id: int, db: AsyncSession = Depends(get_db)):
    res = await db.execute(
        select(MemberModel).where(MemberModel.id == member_id)
    )
    member = res.scalars().first()

    if not member:
        raise HTTPException(status_code=404, detail="Member not found")

    return member


@router.delete("/{member_id}")
async def delete_member_handler(member_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await delete_member(db, member_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Member not found")
    return {"status": "deleted"}