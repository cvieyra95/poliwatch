from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import get_db
import models as models
from app.schemas import PostCommittee

router = APIRouter(prefix="/committees", tags=["committees"])
db_dependency = Annotated[Session, Depends(get_db)]

# POST /committees
@router.post("/", status_code=status.HTTP_201_CREATED)
def create_committee(cmt: PostCommittee, db: db_dependency):
    if cmt.parent_committee_id is not None:
        exists = db.query(models.Committee.id).filter(
            models.Committee.id == cmt.parent_committee_id
        ).first()
        if not exists:
            raise HTTPException(status_code=404, detail="parent_committee_id not found")

    db_cmt = models.Committee(
        chamber=cmt.chamber,
        external_id=cmt.external_id,
        name=cmt.name,
        parent_committee_id=cmt.parent_committee_id,
    )
    db.add(db_cmt)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        # external_id is unique
        raise HTTPException(status_code=409, detail="external_id already exists")
    db.refresh(db_cmt)
    return {"id": db_cmt.id}

# GET /committees/{committee_id}
@router.get("/{committee_id}", status_code=status.HTTP_200_OK)
def read_committee(committee_id: int, db: db_dependency):
    c = db.query(models.Committee).filter(models.Committee.id == committee_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Committee not found")
    return {
        "id": c.id,
        "chamber": c.chamber,
        "external_id": c.external_id,
        "name": c.name,
        "parent_committee_id": c.parent_committee_id,
    }

# GET /committees/by-external/{external_id}
@router.get("/by-external/{external_id}", status_code=status.HTTP_200_OK)
def read_committee_by_external(external_id: str, db: db_dependency):
    c = db.query(models.Committee).filter(models.Committee.external_id == external_id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Committee not found")
    return {
        "id": c.id,
        "chamber": c.chamber,
        "external_id": c.external_id,
        "name": c.name,
        "parent_committee_id": c.parent_committee_id,
    }

# GET /committees/{committee_id}/subcommittees
@router.get("/{committee_id}/subcommittees", status_code=status.HTTP_200_OK)
def list_subcommittees(committee_id: int, db: db_dependency):
    rows = (
        db.query(models.Committee)
        .filter(models.Committee.parent_committee_id == committee_id)
        .order_by(models.Committee.name)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=404, detail="No subcommittees for this committee_id")
    return [
        {
            "id": r.id,
            "chamber": r.chamber,
            "external_id": r.external_id,
            "name": r.name,
            "parent_committee_id": r.parent_committee_id,
        }
        for r in rows
    ]