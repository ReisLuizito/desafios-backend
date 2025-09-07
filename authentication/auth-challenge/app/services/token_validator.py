from typing import Protocol

class TokenValidator(Protocol):
    def is_valid(self, token: str) -> bool: ...

class StaticTokenValidator:
    """
    Validador simples que compara com um token estático (via env).
    Substitua por uma implementação real (JWT/HMAC/OAuth) quando quiser.
    """
    def __init__(self, expected: str):
        self.expected = expected

    def is_valid(self, token: str) -> bool:
        return token == self.expected
