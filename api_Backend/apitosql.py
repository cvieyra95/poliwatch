import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models as models                 
from database import engine             

# Routers
from app.router.members      import router as members_router
from app.router.member_terms import router as member_term_router
from app.router.bills        import router as bills_router    # uncomment when you add /bills
from app.router.vote         import router as vote_router
from app.router.vote_records import router as vote_records_router
from app.router.committees import router as committees_router
from app.router.committee_memberships import router as committee_memberships_router

app = FastAPI()

_allowed = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "").split(",") if o.strip()]
if not _allowed:
    _allowed = ["http://localhost:5173"]  # safe dev fallback

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed,
    allow_credentials=False,              # leave False unless you do cookie auth
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Create tables once at startup (not at import-time)
@app.on_event("startup")
def _init_db():
    models.Base.metadata.create_all(bind=engine)

# Mount routers
app.include_router(members_router)
app.include_router(member_term_router)
app.include_router(bills_router)
app.include_router(vote_router)
app.include_router(vote_records_router)
app.include_router(committees_router)
app.include_router(committee_memberships_router)