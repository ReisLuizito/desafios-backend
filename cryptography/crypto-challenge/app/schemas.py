from pydantic import BaseModel, Field

class PaymentBase(BaseModel):
    userDocument: str = Field(..., examples=["36140781833"])
    creditCardToken: str = Field(..., examples=["abc123"])
    value: int = Field(..., ge=0, examples=[5999])

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int

    class Config:
        from_attributes = True

class PaymentUpdate(BaseModel):
    userDocument: str | None = None
    creditCardToken: str | None = None
    value: int | None = None
