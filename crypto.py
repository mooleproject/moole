# common/crypto.py
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

def aes_encrypt(key: bytes, plaintext: bytes) -> bytes:
    aes = AESGCM(key)
    nonce = b'000000000000'
    return nonce + aes.encrypt(nonce, plaintext, None)

def aes_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    aes = AESGCM(key)
    nonce = ciphertext[:12]
    body = ciphertext[12:]
    return aes.decrypt(nonce, body, None)
