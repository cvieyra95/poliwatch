from __future__ import annotations
import argparse
from database import SessionLocal
import models as models
from app.ingest.congressapi_client import CongressClient
from app.ingest.mappers import normalize_member, normalize_terms
from app.ingest.load_member_terms import upsert_terms
from typing import Iterable


def upsert_terms(db, member_id: int, terms: Iterable[dict]) -> int:
    """
    Insert any terms for this member that don't already exist.
    Returns how many rows were added.
    """
    # 1) load what's already there for this member
    existing = {
        (t.chamber, t.state, t.district, t.start_date, t.end_date)
        for t in db.query(models.MemberTerm).filter(models.MemberTerm.member_id == member_id)
    }

    # 2) build new rows, skipping duplicates
    to_add = []
    for t in terms:
        key = (t["chamber"], t["state"], t["district"], t["start_date"], t["end_date"])
        if key in existing:
            continue
        to_add.append(models.MemberTerm(member_id=member_id, **t))

    # 3) stage inserts (commit happens in your page loop)
    if to_add:
        db.add_all(to_add)
    return len(to_add)

def upsert_member(db, data: dict) -> models.Member:
    m = db.query(models.Member).filter(models.Member.bioguide_id == data["bioguide_id"]).first()
    if not m:
        m = models.Member(bioguide_id=data["bioguide_id"])
        db.add(m)
    # snapshot fields
    m.first_name        = data["first_name"]
    m.middle_name       = data["middle_name"]
    m.last_name         = data["last_name"]
    m.display_name      = data["display_name"]
    m.img_url           = data["img_url"]
    m.profile_url       = data["profile_url"]
    m.in_office         = data["in_office"]
    m.party             = data["party"]
    m.state             = data["state"]
    # enforce Senate rule
    m.district          = None if data["chamber"].value == "Senate" else data["district"]
    m.chamber           = data["chamber"]
    m.source_updated_at = data["source_updated_at"]
    return m

def upsert_terms(db, member_id: int, terms: list[dict]) -> int:
    # current rows for this member -> build a de-dup set
    existing = {
        (t.chamber, t.state, t.district, t.start_date, t.end_date)
        for t in db.query(models.MemberTerm)
                   .filter(models.MemberTerm.member_id == member_id)
    }

    to_add = []
    for t in (terms or []):
        key = (t["chamber"], t["state"], t.get("district"), t["start_date"], t.get("end_date"))
        if key in existing:
            continue
        to_add.append(models.MemberTerm(member_id=member_id, **t))
        existing.add(key)  # keep the set in sync to avoid dupes within this call

    if to_add:
        db.add_all(to_add)

    return len(to_add)

def run(pages: int | None, start_offset: int = 0):
    client = CongressClient()
    db = SessionLocal()
    try:
        processed = 0
        offset = start_offset
        while True:
            items, next_offset = client.get_members_page(offset)
            if not items:
                break

            page_added = 0

            for it in items:
                mem = normalize_member(it)
                obj = upsert_member(db, mem)

                db.flush()                   # ensure obj.id is available
                terms = normalize_terms(it)  # build clean term dicts
                added = upsert_terms(db, obj.id, terms)
                page_added += added
                
                processed += 1

            db.commit()  # commit once per page
            print(f"[PAGE] offset={offset} members={len(items)} terms_added={page_added}")

            if pages is not None:
                pages -= 1
                if pages <= 0:
                    break
            if next_offset is None:
                break
            offset = next_offset

        print(f"Done. Processed: {processed}")
    finally:
        db.close()
        client.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=int, default=1, help="How many pages to fetch (None = all)")
    ap.add_argument("--offset", type=int, default=0)
    args = ap.parse_args()
    run(args.pages, args.offset)