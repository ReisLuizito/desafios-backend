from fastapi import FastAPI
from app.schemas import CustomerRequest, CustomerLoansResponse
from app.services import determine_loans

app = FastAPI(title="Loan Challenge")

@app.post("/customer-loans", response_model=CustomerLoansResponse)
def customer_loans(customer: CustomerRequest):
    loans = determine_loans(customer)
    return CustomerLoansResponse(customer=customer.name, loans=loans)
