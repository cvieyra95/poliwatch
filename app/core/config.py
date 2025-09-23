from pydantic import BaseModel
import os

class Settings(BaseModel):
    env: str = os.getenv("ENV", "dev")
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./local.db")
    congress_api_key: str = os.getenv("CONGRESS_API_KEY", "")
    other1_api_key: str = os.getenv("OTHER1_API_KEY", "")
    other2_api_key: str = os.getenv("OTHER2_API_KEY", "")

settings = Settings()
