from pydantic import BaseModel, Field

class PasswordRequest(BaseModel):
    password: str = Field(..., min_length=1)

class ValidationError(BaseModel):
    code: str
    message: str
