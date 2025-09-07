from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Token estático de exemplo. Em produção você trocaria por algo mais robusto (JWT, HMAC, etc.)
    AUTH_TOKEN: str = "vYQIYxOpyfr=="

    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="", extra="ignore"
    )

settings = Settings()
