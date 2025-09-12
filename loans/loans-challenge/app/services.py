from app.schemas import CustomerRequest, LoanOption

def determine_loans(customer: CustomerRequest) -> list[LoanOption]:
    loans: list[LoanOption] = []

    if customer.income <= 3000 or (
        3000 < customer.income <= 5000
        and customer.age < 30
        and customer.location.upper() == "SP"
    ):
        loans.append(LoanOption(type="PERSONAL", interest_rate=4))

    if customer.income >= 5000:
        loans.append(LoanOption(type="CONSIGNMENT", interest_rate=2))

    if customer.income <= 3000 or (
        3000 < customer.income <= 5000
        and customer.age < 30
        and customer.location.upper() == "SP"
    ):
        loans.append(LoanOption(type="GUARANTEED", interest_rate=3))

    return loans
