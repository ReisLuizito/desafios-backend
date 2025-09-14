from fastapi import FastAPI, HTTPException, status
from app.schemas import PasswordRequest
from app.services import validate_password

app = FastAPI(title="Secure Password Challenge")

@app.post("/validate-password", status_code=status.HTTP_204_NO_CONTENT)
def validate_password_endpoint(payload: PasswordRequest):
    errors = validate_password(payload.password)
    if errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=[e.model_dump() for e in errors],
        )
    return
