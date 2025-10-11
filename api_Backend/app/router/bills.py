from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session

from database import get_db
import models as models
from app.schemas import PostBill  


router = APIRouter(prefix="/bills", tags=["bills"])
db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_bill(bill: PostBill, db: db_dependency):
    # ensure FK exists
    if bill.sponsor_member_id is not None:
        exists = db.query(models.Member.id).filter(models.Member.id == bill.sponsor_member_id).first()
        if not exists:
            raise HTTPException(status_code=404, detail="sponsor_member_id not found")
        
    db_bill = models.Bill(
        #bill_id           = bill.bill_id,
        congress          = bill.congress,
        bill_type         = bill.bill_type,
        number            = bill.number,
        title             = bill.title,
        introduced_date   = bill.introduced_date,
        sponsor_member_id = bill.sponsor_member_id        
    )
    db.add(db_bill)
    db.commit()
    db.refresh(db_bill)
    return {"id": db_bill.id}

@router.get("/{bill_id}", status_code=status.HTTP_200_OK)
def read_bill(bill_id: int, db: db_dependency):
    b = db.query(models.Bill).filter(models.Bill.id == bill_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {
        "id": b.id,
        "congress": b.congress,
        "bill_type": b.bill_type,
        "number": b.number,
        "title": b.title,
        "introduced_date": b.introduced_date,
        "sponsor_member_id": b.sponsor_member_id,
    }

@router.get("/by-key/{congress}/{bill_type}/{number}", status_code=status.HTTP_200_OK)
def read_bill_by_key(congress: int, bill_type: str, number: int, db: db_dependency):
    b = (
        db.query(models.Bill)
        .filter(
            models.Bill.congress == congress,
            models.Bill.bill_type == bill_type,
            models.Bill.number == number,
        )
        .first()
    )
    if not b:
        raise HTTPException(status_code=404, detail="Bill not found")
    return {
        "id": b.id,
        "congress": b.congress,
        "bill_type": b.bill_type,
        "number": b.number,
        "title": b.title,
        "introduced_date": b.introduced_date,
        "sponsor_member_id": b.sponsor_member_id,
    }

#