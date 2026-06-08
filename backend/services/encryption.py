import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from backend.config import ENCRYPTION_KEY


def _derive_key() -> bytes:
    raw = ENCRYPTION_KEY.encode("utf-8")
    if len(raw) < 32:
        raw = raw.ljust(32, b"\x00")
    return raw[:32]


KEY = _derive_key()


def encrypt(plaintext: str) -> str:
    nonce = os.urandom(12)
    aesgcm = AESGCM(KEY)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    combined = nonce + ciphertext
    return base64.b64encode(combined).decode("utf-8")


def decrypt(encoded: str) -> str:
    combined = base64.b64decode(encoded.encode("utf-8"))
    nonce = combined[:12]
    ciphertext = combined[12:]
    aesgcm = AESGCM(KEY)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf-8")
