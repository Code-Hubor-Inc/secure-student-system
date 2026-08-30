import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings


def _get_master_key() -> bytes:
    return hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()


def _wrap_dek(dek: bytes) -> bytes:
    master_key = _get_master_key()
    aesgcm = AESGCM(master_key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, dek, None)
    return nonce + ciphertext


def _unwrap_dek(wrapped_dek: bytes) -> bytes:
    master_key = _get_master_key()
    aesgcm = AESGCM(master_key)
    nonce, ciphertext = wrapped_dek[:12], wrapped_dek[12:]
    return aesgcm.decrypt(nonce, ciphertext, None)


def encrypt_file(plaintext: bytes) -> tuple[bytes, bytes, bytes]:
    dek = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    aesgcm = AESGCM(dek)
    ciphertext = aesgcm.encrypt(nonce, plaintext, None)
    encrypted_dek = _wrap_dek(dek)
    return ciphertext, encrypted_dek, nonce


def decrypt_file(ciphertext: bytes, encrypted_dek: bytes, nonce: bytes) -> bytes:
    dek = _unwrap_dek(encrypted_dek)
    aesgcm = AESGCM(dek)
    return aesgcm.decrypt(nonce, ciphertext, None)
