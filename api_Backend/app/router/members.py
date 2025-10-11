from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
import models as models
from app.schemas import PostMembers

router = APIRouter(prefix="/members", tags=["members"])
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED) #Good
def create_member(member: PostMembers, db: db_dependency):
    db_member = models.Member(
        bioguide_id       = member.bioguide_id,
        first_name        = member.first_name,
        middle_name       = member.middle_name,
        last_name         = member.last_name,
        display_name      = member.display_name,
        img_url           = member.img_url,
        profile_url       = member.profile_url,
        in_office         = member.in_office,
        party             = member.party,
        state             = member.state,
        district          = member.district,
        chamber           = member.chamber,
        created_at        = member.created_at,
        updated_at        = member.updated_at,
        source_updated_at = member.source_updated_at
    )
    db.add(db_member)
    db.commit()
    db.refresh(db_member)
    return {"id": db_member.id}


@router.get("/{b_id}", status_code=status.HTTP_200_OK) #good
def read_member(b_id: str, db: db_dependency):
    member = db.query(models.Member).filter(models.Member.bioguide_id == b_id).first()
    if member is None:
        raise HTTPException(status_code=404, detail="Member not in system")
    return {
        "id":          member.id,
        "bioguide_id": member.bioguide_id,
        "first_name":  member.first_name,
        "last_name":   member.last_name,
        "in_office":   member.in_office,
        "party":       member.party,
        "state":       member.state,
        "district":    member.district,
        "chamber":     member.chamber,
    }

