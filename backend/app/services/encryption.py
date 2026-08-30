"""Envelope encryption for uploaded files.

Each file is encrypted with a random, single-use Data Encryption Key (DEK)
using AES-256-GCM. The DEK itself is then "wrapped" (encrypted) with a
master key derived from ``settings.ENCRYPTION_KEY`` so that only the
wrapped DEK, not the master key, needs to be stored per-file.
"""

import hashlib
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from app.core.config import settings

DEK_SIZE = 32  # AES-256
NONCE_SIZE = 12  # 96-bit GCM nonce


def _get_master_key() -> bytes:
    return hashlib.sha256(settings.ENCRYPTION_KEY.encode()).digest()


def _wrap_dek(dek: bytes) -> bytes:
    """Wrap (encrypt) a DEK with the master key.

    Returns ``wrap_nonce || wrapped_dek`` concatenated together so a
    single blob can be stored as ``encrypted_dek``.
    """
    master_key = _get_master_key()
    wrap_nonce = os.urandom(NONCE_SIZE)
    wrapped = AESGCM(master_key).encrypt(wrap_nonce, dek, None)
    return wrap_nonce + wrapped


def _unwrap_dek(wrapped_dek: bytes) -> bytes:
    master_key = _get_master_key()
    wrap_nonce, wrapped = wrapped_dek[:NONCE_SIZE], wrapped_dek[NONCE_SIZE:]
    return AESGCM(master_key).decrypt(wrap_nonce, wrapped, None)


def encrypt_file(data: bytes) -> tuple[bytes, bytes, bytes]:
    """Encrypt ``data`` with a fresh DEK.

    Returns ``(ciphertext, wrapped_dek, nonce)``:
      - ``ciphertext``: the file contents encrypted under the DEK.
      - ``wrapped_dek``: the DEK, encrypted under the master key.
      - ``nonce``: the GCM nonce used to encrypt the file contents.
    """
    dek = os.urandom(DEK_SIZE)
    nonce = os.urandom(NONCE_SIZE)
    ciphertext = AESGCM(dek).encrypt(nonce, data, None)
    wrapped_dek = _wrap_dek(dek)
    return ciphertext, wrapped_dek, nonce


def decrypt_file(ciphertext: bytes, wrapped_dek: bytes, nonce: bytes) -> bytes:
    """Reverse of :func:`encrypt_file`."""
    dek = _unwrap_dek(wrapped_dek)
    return AESGCM(dek).decrypt(nonce, ciphertext, None)
