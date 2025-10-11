from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
import models as models
from app.schemas import PostMemberTerm  


router = APIRouter(prefix="/members_terms", tags=["members_terms"])
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_member_term(term: PostMemberTerm, db: db_dependency):
    # ensure FK exists
    exists = db.query(models.Member.id).filter(models.Member.id == term.member_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="member_id not found")

    db_term = models.MemberTerm(
        member_id  = term.member_id,
        congress = term.congress,
        chamber    = term.chamber,
        state      = term.state,
        district   = term.district,
        party      = term.party,
        start_year = term.start_year,
        end_year   = term.end_year,
    )
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return {"id": db_term.id}

@router.get("/{member_id}", status_code=status.HTTP_200_OK)
def read_member_terms(member_id: int, db: db_dependency):
    exists = db.query(models.Member.id).filter(models.Member.id == member_id).first()
    if not exists:
        raise HTTPException(status_code=404, detail="member_id not found")

    terms = (
        db.query(models.MemberTerm)
        .filter(models.MemberTerm.member_id == member_id)
        .order_by(models.MemberTerm.congress, models.MemberTerm.start_year)
        .all()
    )
    if not terms:
        raise HTTPException(status_code=404, detail="No terms for this member_id")

    return [
        {
            "id": t.id,
            "member_id": t.member_id,
            "congress": t.congress,
            "chamber": t.chamber,
            "state": t.state,
            "district": t.district,
            "party": t.party,
            "start_year": t.start_year,
            "end_year": t.end_year,
        }
        for t in terms
    ]
