# app/scripts/smoke_db.py
from sqlalchemy import select, func
from app.db.session import SessionLocal
from app.db.models import Member

def main():
    db = SessionLocal()
    try:
        # insert a dummy member
        m = Member(first_name="Test", last_name="User")
        db.add(m)
        db.commit()
        db.refresh(m)
        print("Inserted Member id:", m.id)

        # count members
        total = db.scalar(select(func.count()).select_from(Member))
        print("Members in DB:", total)

    finally:
        db.close()

if __name__ == "__main__":
    main()
