from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SIGNING_SECRET: str = "change_me_32_chars_or_more"
    DATABASE_URL: str = "sqlite:///./transfers.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

settings = Settings()