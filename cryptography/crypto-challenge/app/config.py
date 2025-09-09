from pydantic_settings import BaseSettings, SettingsConfigDict
import base64

class Settings(BaseSettings):
    ENCRYPTION_KEY: str
    DATABASE_URL: str = "sqlite:///./crypto.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")

    @property
    def encryption_key_bytes(self) -> bytes:
        # chave em base64 urlsafe -> bytes
        return base64.urlsafe_b64decode(self.ENCRYPTION_KEY)

settings = Settings()
