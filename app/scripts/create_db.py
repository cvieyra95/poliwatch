from app.db.base import Base   # this also imports models via base.py
from app.db.session import engine
import app.db.models 

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("Tables created.")
