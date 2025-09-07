from fastapi import FastAPI, Response
from app.config import settings
from app.middleware.auth import AuthMiddleware
from app.services.token_validator import StaticTokenValidator

app = FastAPI(title="Auth Challenge")

# Middleware de autenticação aplicado globalmente (protege endpoints atuais e futuros)
app.add_middleware(AuthMiddleware, validator=StaticTokenValidator(settings.AUTH_TOKEN))

@app.get("/health")
def health():
    return {"status": "ok"}

# Endpoint de exemplo do enunciado: deve responder 204 No Content se token válido
@app.get("/foo-bar")
def foo_bar():
    return Response(status_code=204)

# Um segundo endpoint para demonstrar que novos endpoints continuam protegidos
@app.get("/another")
def another():
    return {"ok": True}
