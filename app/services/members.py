# app/services/members.py
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Member

def get_member_by_id(db: Session, member_id: int) -> Member | None:
    return db.get(Member, member_id)

def list_members(db: Session, state: str | None = None, chamber: str | None = None) -> list[Member]:
    stmt = select(Member)
    if state:
        stmt = stmt.where(Member.state == state)
    if chamber:
        stmt = stmt.where(Member.chamber == chamber)
    return db.execute(stmt).scalars().all()
