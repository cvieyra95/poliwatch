from __future__ import annotations
import argparse
from database import SessionLocal
import models
from app.ingest.congressapi_client import CongressClient
from app.ingest.mappers import normalize_terms


def upsert_terms(db, member_id: int, terms: list[dict]) -> int:
    """
    Insert missing terms for a member. We treat the tuple
    (chamber, state, district, start_date, end_date) as a uniqueness key
    and skip duplicates.

    Returns: number of new rows inserted.
    """
    # Load existing terms for this member
    
    terms = terms or []
    existing = db.query(models.MemberTerm).filter(
        models.MemberTerm.member_id == member_id
    ).all()

    # Build a set of existing "keys" so we can skip duplicates
    existing_keys = {(et.congress, et.chamber) for et in existing}

    
    added = 0
    for t in terms:
        key = (t["congress"], t["chamber"])
        if key in existing_keys:
            continue  # already have it

        # Create a new MemberTerm row
        db.add(models.MemberTerm(
            member_id = member_id,
            congress  = t["congress"],
            chamber   = t["chamber"],
            state     = t["state"],
            district  = t["district"],
            party     = t["party"],
            start_year = t["start_year"],
            end_year   = t["end_year"],
        ))
        existing_keys.add(key)
        added += 1

    return added


def run(batch_size: int = 200, start_id: int | None = None):
    """
    Iterate over members already in your DB (in id order), fetch each
    member's detailed record from Congress.gov, normalize the term history,
    and upsert into member_terms.
    """
    client = CongressClient()   # HTTP client with your API key
    db = SessionLocal()         # DB session

    total_added = 0
    processed = 0
    skipped_no_bio = 0
    skipped_no_detail = 0
    normalized_zero = 0

    try:
        # Base query in ascending id order
        base_q = db.query(models.Member).order_by(models.Member.id)
        if start_id:
            base_q = base_q.filter(models.Member.id >= start_id)

        last_id = 0
        while True:
            # Pull a batch of members > last_id to avoid OFFSET performance issues
            batch = (
                base_q.filter(models.Member.id > last_id)
                      .limit(batch_size)
                      .all()
            )
            if not batch:
                break
            batch_added = 0 

            for m in batch:
                last_id = m.id  # advance the cursor

                # --- telemetry: missing bioguide -> skip ---
                if not m.bioguide_id:
                    skipped_no_bio += 1
                    continue

                # Fetch detail from Congress.gov
                detail = client.get_member_detail(m.bioguide_id)
                if not detail:
                    skipped_no_detail += 1
                    continue

                # Convert raw JSON into term rows that fit your schema
                terms = normalize_terms(detail) or []
                if not isinstance(terms, list):
                    # bad contract: force empty list
                    terms = []

                if not terms:
                    normalized_zero += 1

                # Insert only the terms we don't already have
                added = upsert_terms(db, m.id, terms)
                total_added += added
                batch_added += added
                processed += 1

                # Optional noisy trace (uncomment if you want per-member logs)
                # if added > 0:
                #     print(f"[ADD] member_id={m.id} ({m.bioguide_id}) added={added}")

            # Persist the batch of inserts
            db.commit()
            print(f"[STATS] batch_size={len(batch)} processed={processed} "
                    f"added_this_batch={batch_added} total_added={total_added} "
                    f"no_bio={skipped_no_bio} no_detail={skipped_no_detail} empty_terms={normalized_zero}"
                    )


        print(f"Done. Terms inserted: {total_added} "
            f"(processed={processed}, no_bio={skipped_no_bio}, no_detail={skipped_no_detail}, empty_terms={normalized_zero})")


    finally:
        # Clean shutdown of resources
        db.close()
        client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Populate member_terms for members already in the database."
    )
    parser.add_argument("--batch-size", type=int, default=200,
                        help="How many members to process per DB round-trip.")
    parser.add_argument("--start-id", type=int, default=None,
                        help="Start from this Member.id (useful for resumes).")
    args = parser.parse_args()
    run(batch_size=args.batch_size, start_id=args.start_id)
