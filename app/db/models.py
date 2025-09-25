from sqlalchemy import String, Integer, ForeignKey, DateTime, UniqueConstraint, Boolean, Date, Enum, CheckConstraint, func, SmallInteger, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from datetime import datetime

PartyEnum   = Enum("Democratic","Republican","Independent","Libertarian","Other", name="party_enum")
ChamberEnum = Enum("House","Senate", name="chamber_enum")
VotePositionEnum= Enum("Yea","Nay","Present","Not Voting","Absent","Unknown", name="vote_position_enum")
CommitteeRoleEnum = Enum("Chair","Ranking Member","Vice Chair","Member","Ex Officio","Other", name="committee_role_enum")

class Member(Base):
    __tablename__  = "members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    bioguide_id: Mapped[str | None] = mapped_column(String(32), unique=True, index=True)

    # identity
    first_name:  Mapped[str] = mapped_column(String(100), nullable=False)
    middle_name: Mapped[str | None]  = mapped_column(String(50))
    last_name:   Mapped[str] = mapped_column(String(100), nullable=False)
    display_name:Mapped[str | None]  = mapped_column(String(200), index=True)
    img_url:     Mapped[str | None]  = mapped_column(String(300))
    profile_url: Mapped[str | None]  = mapped_column(String(300))

    # current snapshot (mirror active term for fast queries)
    in_office: Mapped[bool]           = mapped_column(Boolean, server_default="0", index=True)
    party:     Mapped[str | None]     = mapped_column(PartyEnum, nullable=True, index=True)
    state:     Mapped[str | None]     = mapped_column(String(2), nullable=True)
    district:  Mapped[int | None]     = mapped_column(SmallInteger, nullable=True)
    chamber:   Mapped[str | None]     = mapped_column(ChamberEnum, nullable=True, index=True)

    created_at:        Mapped[datetime]        = mapped_column(DateTime, server_default=func.now())
    updated_at:        Mapped[datetime]        = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    source_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    # relations
    terms: Mapped[list["MemberTerm"]] = relationship(back_populates="member", cascade="all, delete-orphan")
    vote_records: Mapped[list["VoteRecord"]] = relationship(back_populates="member")
    committee_memberships: Mapped[list["CommitteeMembership"]] = relationship(back_populates="member")

    __table_args__ = (
        CheckConstraint("state IS NULL OR REGEXP_LIKE(state, '^[A-Z]{2}$', 'c')", name="ck_member_state_uc"),
        CheckConstraint("district IS NULL OR (district BETWEEN 0 AND 56)", name="ck_member_district"),
        Index("ix_member_current_seat", "in_office", "state", "district", "chamber"),
    )



class MemberTerm(Base):
    __tablename__ = "member_terms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)

    chamber:  Mapped[str]           = mapped_column(ChamberEnum, index=True)
    state:    Mapped[str]           = mapped_column(String(2))
    district: Mapped[int | None]    = mapped_column(SmallInteger)
    party:    Mapped[str | None]    = mapped_column(PartyEnum)
    start_date: Mapped[datetime]    = mapped_column(DateTime, index=True)
    end_date:   Mapped[datetime | None] = mapped_column(DateTime, index=True)

    member: Mapped["Member"] = relationship(back_populates="terms")

    __table_args__ = (
        CheckConstraint("REGEXP_LIKE(state, '^[A-Z]{2}$', 'c')", name="ck_term_state_uc"),
        CheckConstraint("district IS NULL OR (district BETWEEN 0 AND 56)", name="ck_term_district"),
        CheckConstraint("end_date IS NULL OR end_date >= start_date", name="ck_term_dates"),
        Index("ix_term_member_dates", "member_id", "start_date"),  
    )

class Bill(Base):
    __tablename__ = "bills"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    congress: Mapped[int] = mapped_column(Integer, index=True)
    bill_type: Mapped[str] = mapped_column(String(10), index=True)  # 'HR','S','HRES','SRES','HJRES','SJRES','HCONRES','SCONRES'
    number: Mapped[int] = mapped_column(Integer, index=True)
    title:  Mapped[str | None] = mapped_column(String(500))
    introduced_date: Mapped[datetime | None] = mapped_column(DateTime)
    sponsor_member_id: Mapped[int | None] = mapped_column(ForeignKey("members.id"))
    sponsor: Mapped["Member"] | None = relationship(foreign_keys=[sponsor_member_id], backref="sponsored_bills")

    __table_args__ = (
        UniqueConstraint("congress","bill_type","number", name="uq_bill_identity"),
        Index("ix_bill_sponsor", "sponsor_member_id")
        )

class Vote(Base):
    __tablename__ = "votes"
    id:          Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    congress:    Mapped[int] = mapped_column(Integer, index=True)  # Ex: 117
    session:     Mapped[int] = mapped_column(Integer, index=True)   # Ex:
    chamber:     Mapped[str] = mapped_column(ChamberEnum, index=True)  # Ex: "House"
    roll_number: Mapped[int] = mapped_column(Integer, index=True)   # external id

    question:    Mapped[str] = mapped_column(String(500), nullable=False)  # Ex: "On Passage"
    description: Mapped[str | None] = mapped_column(String(2000))  #
    date:        Mapped[datetime | None] = mapped_column(DateTime, index=True)  # Ex: "2021-03-11T05:00:00Z"

    result:      Mapped[str | None] = mapped_column(String(32))  # Ex: "Passed"
    threshold:  Mapped[str | None] = mapped_column(String(32))  # Ex: "2/3"
    yea_count:   Mapped[int | None] = mapped_column(SmallInteger)  # Ex: 220
    nay_count:   Mapped[int | None] = mapped_column(SmallInteger)  # Ex: 211
    present_count: Mapped[int | None] = mapped_column(SmallInteger)  # Ex: 0
    not_voting_count: Mapped[int | None] = mapped_column(SmallInteger)  # Ex: 4

    bill_id: Mapped[int | None] = mapped_column(ForeignKey("bills.id"), index=True)
    bill:    Mapped["Bill"] | None = relationship(backref="votes")
    records: Mapped[list["VoteRecord"]] = relationship( back_populates="vote", cascade="all, delete-orphan",)
    
    __table_args__ = (
        UniqueConstraint("congress","session","chamber","roll_number", name="uq_vote_roll_unique"),
        CheckConstraint("session IN (1,2)", name="ck_vote_session"),
        CheckConstraint("roll_number > 0", name="ck_vote_roll_positive"),
        Index("ix_vote_day_chamber", "date", "chamber"),
    )

class VoteRecord(Base):
    __tablename__ = "vote_records"

    # Composite PK: a member can have at most one record per vote
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), primary_key=True, index=True)
    vote_id:   Mapped[int] = mapped_column(ForeignKey("votes.id", ondelete="CASCADE"), primary_key=True, index=True)

    member: Mapped["Member"] = relationship(back_populates="vote_records", passive_deletes=True)
    vote:   Mapped["Vote"]   = relationship(back_populates="records",       passive_deletes=True)


    position:  Mapped[str] = mapped_column(VotePositionEnum, nullable=False, server_default="Unknown")

    __table_args__ = (
        Index("ix_vr_vote_position", "vote_id", "position"),
        Index("ix_vr_member", "member_id"),
    )

class Committee(Base):
    __tablename__ = "committees"

    id:          Mapped[int]        = mapped_column(Integer, primary_key=True, index=True)
    chamber:     Mapped[str | None] = mapped_column(ChamberEnum, nullable=True, index=True)
    external_id: Mapped[str]        = mapped_column(String(64), unique=True, index=True)   # e.g., "HSAG"
    name:        Mapped[str]        = mapped_column(String(300))

    # subcommittees
    parent_committee_id: Mapped[int | None] = mapped_column(ForeignKey("committees.id", ondelete="CASCADE"), nullable=True)
    parent_committee: Mapped["Committee"] = relationship(remote_side=[id])

    memberships: Mapped[list["CommitteeMembership"]] = relationship(
        back_populates="committee",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        # Fallback uniqueness if external_id is ever missing/buggy
        Index("ix_committee_chamber_name", "chamber", "name"),
    )


class CommitteeMembership(Base):
    __tablename__ = "committee_memberships"

    # You can use a composite PK, but a surrogate id + unique pair is fine too
    id:          Mapped[int] = mapped_column(Integer, primary_key=True)
    member_id:   Mapped[int] = mapped_column(ForeignKey("members.id", ondelete="CASCADE"), index=True)
    committee_id:Mapped[int] = mapped_column(ForeignKey("committees.id", ondelete="CASCADE"), index=True)

    role:        Mapped[str | None] = mapped_column(CommitteeRoleEnum, nullable=True)
    start_date:  Mapped[Date | None] = mapped_column(Date, nullable=True)
    end_date:    Mapped[Date | None] = mapped_column(Date, nullable=True)

    member:   Mapped["Member"]    = relationship(back_populates="committee_memberships")
    committee:Mapped["Committee"] = relationship(back_populates="memberships")

    __table_args__ = (
        UniqueConstraint("member_id","committee_id","start_date", name="uq_member_committee_span"),
    )
