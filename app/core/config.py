from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    CONGRESS_API_KEY: str
    CONGRESS_BASE_URL: str = "https://api.congress.gov/v3"
    APP_NAME: str = "Poliwatch API"
    LOG_LEVEL: str = "INFO"

    ENV: str = "dev"
    OTHER1_API_KEY: str | None = None
    OTHER2_API_KEY: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="forbid")

settings = Settings()
