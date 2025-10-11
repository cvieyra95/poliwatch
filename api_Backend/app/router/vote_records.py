from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
import models as models
from app.schemas import PostVoteRecord

router = APIRouter(prefix="/vote_records", tags=["vote_records"])
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote_record(record: PostVoteRecord, db: db_dependency):
    # FK checks use the payload, not a DB object that doesn't exist yet
    if not db.query(models.Member.id).filter(models.Member.id == record.member_id).first():
        raise HTTPException(status_code=404, detail="member_id not found")
    if not db.query(models.Vote.id).filter(models.Vote.id == record.vote_id).first():
        raise HTTPException(status_code=404, detail="vote_id not found")

    # now create the row
    db_record = models.VoteRecord(
        member_id=record.member_id,
        vote_id=record.vote_id,
        position=record.position,
    )
    db.add(db_record)
    db.commit()
    # composite PK: nothing to refresh; both keys come from payload
    return {"member_id": db_record.member_id, "vote_id": db_record.vote_id, "position": db_record.position}


@router.get("/{vote_id}/{member_id}", status_code=status.HTTP_200_OK)
def read_vote_record(vote_id: int, member_id: int, db: db_dependency):
    voting_record = (
        db.query(models.VoteRecord).filter(models.VoteRecord.vote_id == vote_id,models.VoteRecord.member_id == member_id).first()
    )
    if not voting_record:
        raise HTTPException(status_code=404, detail="VoteRecord not found")
    return {"member_id": voting_record.member_id, "vote_id": voting_record.vote_id, "position": voting_record.position}

@router.get("/by-vote/{vote_id}", status_code=status.HTTP_200_OK)
def list_vote_records_by_vote(vote_id: int, db: db_dependency):
    rows = (
        db.query(models.VoteRecord)
        .filter(models.VoteRecord.vote_id == vote_id)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No vote records for this vote_id")
    return [{"member_id": r.member_id, "vote_id": r.vote_id, "position": r.position} for r in rows]

@router.get("/by-member/{member_id}", status_code=status.HTTP_200_OK)
def list_vote_records_by_member(member_id: int, db: db_dependency):
    rows = (
        db.query(models.VoteRecord)
        .filter(models.VoteRecord.member_id == member_id)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No vote records for this member_id")
    return [{"member_id": r.member_id, "vote_id": r.vote_id, "position": r.position} for r in rows]