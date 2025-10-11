from __future__ import annotations
from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, Field, StringConstraints, model_validator
from enums import Party, Chamber, BillType, VotePosition, CommitteeRole   

Refined_state = Annotated[str, StringConstraints(pattern=r"^[A-Z]{2}$")]

class PostMembers(BaseModel):
    bioguide_id:       str
    first_name:        str
    middle_name:       Optional[str] = None
    last_name:         str
    display_name:      Optional[str] = None
    img_url:           Optional[str] = None
    profile_url:       Optional[str] = None
    in_office:         bool
    party:             Optional[Party] = None
    state:             Refined_state
    district:          Optional[int] = Field(default=None, ge=0, le=56)
    chamber:           Chamber
    created_at:        Optional[datetime] = None
    updated_at:        Optional[datetime] = None
    source_updated_at: Optional[datetime] = None

    @model_validator(mode="after")
    def _senate_requires_no_district(self):
        # Enforce: Senate terms do not have districts
        if self.chamber == Chamber.Senate and self.district is not None:
            raise ValueError("Senate members must have district=None.")
        return self

class PostMemberTerm(BaseModel):
    member_id: int
    congress: int
    chamber: Chamber
    state: Refined_state
    district: Optional[int] = Field(default=None, ge=0, le=56)
    party: Optional[Party] = None
    start_year: int
    end_year: Optional[int] = None

    @model_validator(mode="after")
    def _rules(self):
        if self.chamber == Chamber.Senate and self.district is not None:
            raise ValueError("Senate terms must have district=None.")
        if self.end_year is not None and self.end_year < self.start_year:
            raise ValueError("end_year must be >= start_year.")
        return self
    
class PostBill(BaseModel):
    #bill_id: int
    congress: int
    bill_type: BillType           
    number: int
    title: Optional[str] = None
    introduced_date: Optional[datetime] = None
    sponsor_member_id: Optional[int] = None

class PostVote(BaseModel):
    congress: int
    session: int = Field(..., ge=1, le=2)      
    chamber: Chamber                         # 
    roll_number: int = Field(..., gt=0)            # > 0

    question: str
    description: Optional[str]      = None
    date: Optional[datetime]        = None

    result: Optional[str]           = None
    threshold: Optional[str]        = None
    yea_count: Optional[int]        = Field(default=None, ge=0)
    nay_count: Optional[int]        = Field(default=None, ge=0)
    present_count: Optional[int]    = Field(default=None, ge=0)
    not_voting_count: Optional[int] = Field(default=None, ge=0)

    bill_id: Optional[int] = None                  # FK to bills.id (nullable)

class PostVoteRecord(BaseModel):
    member_id: int = Field(..., gt=0)
    vote_id:   int = Field(..., gt=0)
    position:  VotePosition 

class PostCommittee(BaseModel):
    chamber: Optional[Chamber] = None
    external_id: str
    name: str
    parent_committee_id: Optional[int] = None

class PostCommitteeMembership(BaseModel):
    member_id: int = Field(..., gt=0)
    committee_id: int = Field(..., gt=0)
    role: Optional[CommitteeRole] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    @model_validator(mode="after")
    def _dates_ok(self):
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValueError("end_date must be >= start_date.")
        return self


class IdOut(BaseModel):
    id: int