from pydantic import BaseModel, Field, ConfigDict

class TransferIn(BaseModel):
    amount: int = Field(..., ge=0)
    currency: str = Field(..., min_length=3, max_length=8)
    beneficiary_account: str = Field(..., min_length=3, max_length=128)

class TransferOut(BaseModel):
    id: int
    amount: int
    currency: str
    beneficiary_account: str

    model_config = ConfigDict(from_attributes=True)