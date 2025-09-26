# app/api/v1/members.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.schemas.members import MemberOut
from app.services.members import get_member_by_id, list_members

router = APIRouter(prefix="/members", tags=["members"])

@router.get("/{member_id}", response_model=MemberOut)
def read_member(member_id: int, db: Session = Depends(get_db)):
    m = get_member_by_id(db, member_id)
    if not m:
        raise HTTPException(404, "Member not found")
    return m

@router.get("/", response_model=list[MemberOut])
def read_members(state: str | None = None, chamber: str | None = None, db: Session = Depends(get_db)):
    return list_members(db, state=state, chamber=chamber)
