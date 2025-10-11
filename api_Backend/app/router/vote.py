from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
import models as models
from app.schemas import PostVote

router = APIRouter(prefix="/vote", tags=["vote"])
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: PostVote, db: db_dependency):
    db_vote = models.Vote(
        congress = vote.congress,
        session = vote.session,
        chamber = vote.chamber,
        roll_number = vote.roll_number,
        question = vote.question,
        description = vote.description,
        date = vote.date,
        result = vote.result,
        threshold = vote.threshold,
        yea_count = vote.yea_count,
        nay_count = vote.nay_count,
        present_count = vote.present_count,
        not_voting_count = vote.not_voting_count,
        bill_id = vote.bill_id
    )
    db.add(db_vote)
    db.commit()
    db.refresh(db_vote)
    return {"id": db_vote.id}

@router.get("/{vote_id}", status_code=status.HTTP_200_OK)
def read_vote(vote_id: int, db: db_dependency):
    v = db.query(models.Vote).filter(models.Vote.id == vote_id).first()
    if not v:
        raise HTTPException(status_code=404, detail="Vote not found")
    return {
        "id": v.id,
        "congress": v.congress,
        "session": v.session,
        "chamber": v.chamber,
        "roll_number": v.roll_number,
        "question": v.question,
        "description": v.description,
        "date": v.date,
        "result": v.result,
        "threshold": v.threshold,
        "yea_count": v.yea_count,
        "nay_count": v.nay_count,
        "present_count": v.present_count,
        "not_voting_count": v.not_voting_count,
        "bill_id": v.bill_id,
    }

@router.get("/by-key/{congress}/{session}/{chamber}/{roll_number}", status_code=status.HTTP_200_OK)
def read_vote_by_key(congress: int, session: int, chamber: str, roll_number: int, db: db_dependency):
    v = (
        db.query(models.Vote)
        .filter(
            models.Vote.congress == congress,
            models.Vote.session == session,
            models.Vote.chamber == chamber,
            models.Vote.roll_number == roll_number,
        )
        .first()
    )
    if not v:
        raise HTTPException(status_code=404, detail="Vote not found")
    return {
        "id": v.id,
        "congress": v.congress,
        "session": v.session,
        "chamber": v.chamber,
        "roll_number": v.roll_number,
        "question": v.question,
        "description": v.description,
        "date": v.date,
        "result": v.result,
        "threshold": v.threshold,
        "yea_count": v.yea_count,
        "nay_count": v.nay_count,
        "present_count": v.present_count,
        "not_voting_count": v.not_voting_count,
        "bill_id": v.bill_id,
    }

@router.get("/by-bill/{bill_id}", status_code=status.HTTP_200_OK)
def list_votes_by_bill(bill_id: int, db: db_dependency):
    votes = (
        db.query(models.Vote)
        .filter(models.Vote.bill_id == bill_id)
        .order_by(models.Vote.date, models.Vote.roll_number)
        .all()
    )
    if not votes:
        raise HTTPException(status_code=404, detail="No votes for this bill_id")
    return [
        {
            "id": v.id,
            "congress": v.congress,
            "session": v.session,
            "chamber": v.chamber,
            "roll_number": v.roll_number,
            "question": v.question,
            "description": v.description,
            "date": v.date,
            "result": v.result,
            "threshold": v.threshold,
            "yea_count": v.yea_count,
            "nay_count": v.nay_count,
            "present_count": v.present_count,
            "not_voting_count": v.not_voting_count,
            "bill_id": v.bill_id,
        }
        for v in votes
    ]