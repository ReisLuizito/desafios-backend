from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    AUTH_TOKEN: str = "vYQIYxOpyfr=="

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="", extra="ignore"
    )

settings = Settings()
