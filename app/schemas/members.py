from pydantic import BaseModel

class MemberBase(BaseModel):
    bioguide_id: str | None = None
    first_name: str
    last_name: str
    party: str | None = None
    state: str | None = None
    chamber: str | None = None

class MemberOut(MemberBase):
    id: int
    class Config:
        from_attributes = True
