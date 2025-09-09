import os
import base64
from sqlalchemy.types import TypeDecorator, String
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

class EncryptedString(TypeDecorator):
    """
    Armazena no banco uma string encriptada (base64).
    Ao ler do banco, decripta e retorna o plaintext.
    Transparente para a aplicação.
    """
    impl = String
    cache_ok = True

    def __init__(self, key_bytes: bytes, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not key_bytes or len(key_bytes) < 32:  # 256-bit
            raise ValueError("ENCRYPTION_KEY inválida. Gere 32 bytes e codifique em base64 urlsafe.")
        self._key = key_bytes

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        if not isinstance(value, str):
            value = str(value)
        aesgcm = AESGCM(self._key)
        nonce = os.urandom(12)  # 96-bit recomendado para GCM
        ct = aesgcm.encrypt(nonce, value.encode("utf-8"), associated_data=None)
        payload = nonce + ct
        return base64.urlsafe_b64encode(payload).decode("utf-8")

    def process_result_value(self, value, dialect):
        if value is None:
            return None
        raw = base64.urlsafe_b64decode(value.encode("utf-8"))
        nonce, ct = raw[:12], raw[12:]
        aesgcm = AESGCM(self._key)
        pt = aesgcm.decrypt(nonce, ct, associated_data=None)
        return pt.decode("utf-8")
