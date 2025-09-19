from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    BASE_URL: str = "http://127.0.0.1:8000"
    DEFAULT_TTL_MINUTES: int = 1440
    CODE_MIN_LENGTH: int = 5
    CODE_MAX_LENGTH: int = 10
    DATABASE_URL: str = "sqlite:///./shortener.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

settings = Settings()
