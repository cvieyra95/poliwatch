from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    CONGRESS_API_KEY: str
    CONGRESS_BASE_URL: str = "https://api.congress.gov/v3"
    APP_NAME: str = "Poliwatch API"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()
