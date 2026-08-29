from cryptography.exceptions import InvalidTag

from app.services.encryption import decrypt_file, encrypt_file


def test_encrypt_decrypt_roundtrip():
    original = b"some plaintext data"
    ciphertext, encrypted_dek, nonce = encrypt_file(original)
    assert ciphertext != original
    assert decrypt_file(ciphertext, encrypted_dek, nonce) == original


def test_tampered_ciphertext_is_rejected():
    original = b"some plaintext data"
    ciphertext, encrypted_dek, nonce = encrypt_file(original)
    tampered = bytes([ciphertext[0] ^ 0xFF]) + ciphertext[1:]
    try:
        decrypt_file(tampered, encrypted_dek, nonce)
        assert False, "expected InvalidTag to be raised"
    except InvalidTag:
        pass