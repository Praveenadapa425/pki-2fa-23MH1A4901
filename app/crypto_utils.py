# File: app/crypto_utils.py

from pathlib import Path
import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization

# --- Key Loading Functions ---

def load_private_key(path: str = "student_private.pem"):
    """Loads a PEM-encoded private key from the project root."""
    # This function was missing, causing the ImportError.
    data = Path(path).read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def load_public_key(path: str):
    """Loads a PEM-encoded public key from the project root."""
    data = Path(path).read_bytes()
    return serialization.load_pem_public_key(data)


# --- Core Cryptographic Operations ---

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """Decrypts the provided seed using the RSA/OAEP algorithm."""
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decode and validate the seed format
    hex_seed = plaintext.decode("utf-8").strip()
    if len(hex_seed) != 64:
        raise ValueError("Decrypted seed must be 64 hex characters long")
    if not all(c in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Decrypted seed contains non-hex characters")

    return hex_seed


# --- Functions for the Final Commit Proof ---

def sign_message(message: str, private_key) -> bytes:
    """Signs a string using the RSA-PSS algorithm."""
    message_bytes = message.encode("utf-8")
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return signature


def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    """Encrypts raw bytes using the RSA/OAEP algorithm."""
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext