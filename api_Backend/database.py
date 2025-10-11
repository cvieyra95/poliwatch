import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.declarative import declarative_base

#URL_DB = "mysql+pymysql://root:4164keeverave.@localhost:3306/poliwatch_api_database" For local work

URL_DB = os.environ.get( # This is for api online
    "DATABASE_URL",
    "mysql+pymysql://root:4164keeverave.@localhost:3306/poliwatch_api_database"  # fallback for local dev
)

def get_db():
    db = SessionLocal()
    try:
        yield db

    finally:
        db.close()


# Communicates with fastapitomysql
engine = create_engine(URL_DB, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
####

# Communcates with database
Base = declarative_base()