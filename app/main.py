from fastapi import FastAPI
from app.api.v1 import members as members_router

app = FastAPI(title="Poliwatch API")
app.include_router(members_router.router, prefix="/v1")
