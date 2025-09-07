from fastapi import FastAPI, Response
from app.config import settings
from app.middleware.auth import AuthMiddleware
from app.services.token_validator import StaticTokenValidator

app = FastAPI(title="Auth Challenge")

app.add_middleware(AuthMiddleware, validator=StaticTokenValidator(settings.AUTH_TOKEN))

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/foo-bar")
def foo_bar():
    return Response(status_code=204)

@app.get("/another")
def another():
    return {"ok": True}
