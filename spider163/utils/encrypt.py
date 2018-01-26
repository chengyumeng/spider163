# coding=utf-8

import base64

from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from cryptography.hazmat.backends import default_backend


def aes(text, sec_key):
    backend = default_backend()
    pad = 16 - len(text) % 16
    text = text + pad * chr(pad)
    cipher = Cipher(
        algorithms.AES(sec_key.encode('utf-8')),
        modes.CBC(b'0102030405060708'),
        backend=backend
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(text.encode('utf-8')) + encryptor.finalize()
    ciphertext = base64.b64encode(ciphertext)
    return ciphertext
