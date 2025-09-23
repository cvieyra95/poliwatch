from sqlalchemy import String, Integer, ForeignKey, DateTime, UniqueConstraint, Boolean, Date, Enum, CheckConstraint, func, SmallInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

PartyEnum   = Enum("Democratic","Republican","Independent","Libertarian","Other", name="party_enum")
ChamberEnum = Enum("House","Senate", name="chamber_enum")

class Member(Base):
    __tablename__  = "members"
    id:          Mapped[int]         = mapped_column(Integer, primary_key=True, index=True) # Unique id to rep for internal db.
    bioguide_id: Mapped[str | None]  = mapped_column(String(32), index=True, unique=True)   # Ex: "L000174" 

    first_name:  Mapped[str]         = mapped_column(String(100))                           # Ex: "Patrick"
    middle_name: Mapped[str | None]  = mapped_column(String(50))                             # Ex: "J." , Might change, need to see how Congress.gov does it. I am pretty sure it is just the initial.
    last_name:   Mapped[str]         = mapped_column(String(100))                           # Ex: "Leahy"
    display_name:Mapped[str | None]  = mapped_column(String(200), index=True)

    img_url:     Mapped[str | None]  = mapped_column(String(300))                           # Ex: "https://www.congress.gov/img/member/l000174_200.jpg"
    profile_url: Mapped[str | None] = mapped_column(String(300))                            # Ex: "https://api.congress.gov/v3/member/L000174?format=json"
    

    in_office:   Mapped[bool]        = mapped_column(Boolean, server_default="0", index=True)
    # start_year:  Mapped[int]         = mapped_column(int(4))                             # Ex: "1975"
    # end_year:    Mapped[int | None]  = mapped_column(int(4))                             # Ex: "None"
    party:       Mapped[str | None]  = mapped_column(PartyEnum, nullable=True, index=True)                            # Ex: "Democrat"
    state:       Mapped[str | None]  = mapped_column(String(2), nullable=True)                             # Ex: "Vermont"
    district:    Mapped[int | None]  = mapped_column(SmallInteger, nullable=True)                             # Ex: "None"
    chamber:     Mapped[str | None]  = mapped_column(ChamberEnum, nullable=True, index=True)                            # Ex: "Senate"

    created_at:        Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at:        Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    

    vote_records: Mapped[list["VoteRecord"]] = relationship(back_populates="member")
    committee_memberships: Mapped[list["CommitteeMembership"]] = relationship(back_populates="member")

    __table_args__ = (
    CheckConstraint("state IS NULL OR REGEXP_LIKE(state, '^[A-Z]{2}$', 'c')", name="ck_member_state_uc"),
    CheckConstraint("district IS NULL OR (district BETWEEN 0 AND 56)", name="ck_member_district"),
    Index("ix_member_current_seat", "in_office", "state", "district", "chamber"),
    )

class Vote(Base):
    __tablename__ = "votes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    roll_number: Mapped[str | None] = mapped_column(String(32), index=True)   # external id
    chamber: Mapped[str | None] = mapped_column(String(16))
    question: Mapped[str | None] = mapped_column(String(500))
    date: Mapped[DateTime | None] = mapped_column(DateTime)

    records: Mapped[list["VoteRecord"]] = relationship(back_populates="vote")
    __table_args__ = (UniqueConstraint("roll_number", "chamber", name="uq_vote_roll_chamber"),)

class VoteRecord(Base):
    __tablename__ = "vote_records"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    vote_id: Mapped[int] = mapped_column(ForeignKey("votes.id", ondelete="CASCADE"), index=True)
    position: Mapped[str | None] = mapped_column(String(16))  # Yea/Nay/Present/Not Voting

    member: Mapped["Member"] = relationship(back_populates="vote_records")
    vote: Mapped["Vote"] = relationship(back_populates="records")
    __table_args__ = (UniqueConstraint("member_id", "vote_id", name="uq_member_vote"),)

class Committee(Base):
    __tablename__ = "committees"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    external_id: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(300))
    chamber: Mapped[str | None] = mapped_column(String(16))

    memberships: Mapped[list["CommitteeMembership"]] = relationship(back_populates="committee")

class CommitteeMembership(Base):
    __tablename__ = "committee_memberships"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    committee_id: Mapped[int] = mapped_column(ForeignKey("committees.id", ondelete="CASCADE"), index=True)
    role: Mapped[str | None] = mapped_column(String(64))  # Chair/Ranking/Member

    member: Mapped["Member"] = relationship(back_populates="committee_memberships")
    committee: Mapped["Committee"] = relationship(back_populates="memberships")
    __table_args__ = (UniqueConstraint("member_id", "committee_id", name="uq_member_committee"),)
