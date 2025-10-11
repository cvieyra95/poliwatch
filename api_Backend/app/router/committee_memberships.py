from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
import models as models
from app.schemas import PostCommitteeMembership

router = APIRouter(prefix="/committee_memberships", tags=["committee_memberships"])
db_dependency = Annotated[Session, Depends(get_db)]

# POST /committee_memberships
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_committee_membership(cm: PostCommitteeMembership, db: db_dependency):
    if not db.query(models.Member.id).filter(models.Member.id == cm.member_id).first():
        raise HTTPException(status_code=404, detail="member_id not found")
    if not db.query(models.Committee.id).filter(models.Committee.id == cm.committee_id).first():
        raise HTTPException(status_code=404, detail="committee_id not found")

    db_cm = models.CommitteeMembership(
        member_id=cm.member_id,
        committee_id=cm.committee_id,
        role=cm.role,
        start_date=cm.start_date,
        end_date=cm.end_date,
    )
    db.add(db_cm)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # violates uq_member_committee_span or FK
        raise HTTPException(status_code=409, detail="Membership already exists for this span")
    db.refresh(db_cm)
    return {"id": db_cm.id}

# GET /committee_memberships/{id}
@router.get("/{id}", status_code=status.HTTP_200_OK)
def read_committee_membership(id: int, db: db_dependency):
    cm = db.query(models.CommitteeMembership).filter(models.CommitteeMembership.id == id).first()
    if not cm:
        raise HTTPException(status_code=404, detail="CommitteeMembership not found")
    return {
        "id": cm.id,
        "member_id": cm.member_id,
        "committee_id": cm.committee_id,
        "role": cm.role,
        "start_date": cm.start_date,
        "end_date": cm.end_date,
    }

# GET /committee_memberships/by-member/{member_id}
@router.get("/by-member/{member_id}", status_code=status.HTTP_200_OK)
def list_memberships_by_member(member_id: int, db: db_dependency):
    rows = (
        db.query(models.CommitteeMembership)
        .filter(models.CommitteeMembership.member_id == member_id)
        .order_by(models.CommitteeMembership.start_date)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No memberships for this member_id")
    return [
        {
            "id": r.id,
            "member_id": r.member_id,
            "committee_id": r.committee_id,
            "role": r.role,
            "start_date": r.start_date,
            "end_date": r.end_date,
        }
        for r in rows
    ]

# GET /committee_memberships/by-committee/{committee_id}
@router.get("/by-committee/{committee_id}", status_code=status.HTTP_200_OK)
def list_memberships_by_committee(committee_id: int, db: db_dependency):
    rows = (
        db.query(models.CommitteeMembership)
        .filter(models.CommitteeMembership.committee_id == committee_id)
        .order_by(models.CommitteeMembership.start_date)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No memberships for this committee_id")
    return [
        {
            "id": r.id,
            "member_id": r.member_id,
            "committee_id": r.committee_id,
            "role": r.role,
            "start_date": r.start_date,
            "end_date": r.end_date,
        }
        for r in rows
    ]