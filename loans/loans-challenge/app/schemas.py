from pydantic import BaseModel, Field

class CustomerRequest(BaseModel):
    age: int = Field(..., ge=0)
    cpf: str
    name: str
    income: float = Field(..., ge=0)
    location: str

class LoanOption(BaseModel):
    type: str
    interest_rate: int

class CustomerLoansResponse(BaseModel):
    customer: str
    loans: list[LoanOption]
