from app.services.encryption import decrypt_file, encrypt_file


def test_encrypt_decrypt_round_trip():
    data = b"the quick brown fox jumps over the lazy dog"

    ciphertext, wrapped_dek, nonce = encrypt_file(data)

    assert ciphertext != data
    assert wrapped_dek != b""
    assert nonce != b""

    plaintext = decrypt_file(ciphertext, wrapped_dek, nonce)
    assert plaintext == data


def test_encrypt_produces_unique_output_each_time():
    data = b"same input bytes"

    ciphertext_1, wrapped_dek_1, nonce_1 = encrypt_file(data)
    ciphertext_2, wrapped_dek_2, nonce_2 = encrypt_file(data)

    assert ciphertext_1 != ciphertext_2
    assert nonce_1 != nonce_2

    assert decrypt_file(ciphertext_1, wrapped_dek_1, nonce_1) == data
    assert decrypt_file(ciphertext_2, wrapped_dek_2, nonce_2) == data
