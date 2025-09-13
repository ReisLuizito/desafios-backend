from pydantic import BaseModel, Field, field_validator

class POICreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)

    @field_validator("name")
    @classmethod
    def strip_name(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("name must not be blank")
        return s

class POIRead(BaseModel):
    id: int
    name: str
    x: int
    y: int

    class Config:
        from_attributes = True
