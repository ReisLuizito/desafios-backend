from typing import Callable, Optional
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from app.services.token_validator import TokenValidator

EXCLUDE_PATHS = {"/health", "/docs", "/openapi.json", "/redoc"}

def _extract_token(auth_header: Optional[str]) -> Optional[str]:
    if not auth_header:
        return None
    parts = auth_header.strip().split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return auth_header.strip()

class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, validator: TokenValidator):
        super().__init__(app)
        self.validator = validator

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path in EXCLUDE_PATHS:
            return await call_next(request)

        token = _extract_token(request.headers.get("Authorization"))

        if not token or not self.validator.is_valid(token):
            return JSONResponse(
                status_code=401,
                content={"detail": "Token de acesso ausente ou inválido (header Authorization)."}
            )

        return await call_next(request)
