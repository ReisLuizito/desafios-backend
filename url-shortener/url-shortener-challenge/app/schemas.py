from pydantic import BaseModel, HttpUrl, Field, ConfigDict

class ShortenRequest(BaseModel):
    url: str

class ShortUrlResponse(BaseModel):
    url: str

class ResolveError(BaseModel):
    detail: str

class CreatedMap(BaseModel):
    code: str
    long_url: str
    model_config = ConfigDict(from_attributes=True)
