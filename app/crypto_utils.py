# File: app/crypto_utils.py (with comments)

from pathlib import Path
import base64
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization

# --- Key Loading Functions ---

def load_private_key(path: str = "student_private.pem"):
    """
    Loads a PEM-encoded private key from a file.
    Assumes the key is not password-protected.

    Args:
        path (str): The file path to the private key. Defaults to "student_private.pem".

    Returns:
        The private key object from the cryptography library.
    """
    data = Path(path).read_bytes()
    return serialization.load_pem_private_key(data, password=None)


def load_public_key(path: str):
    """
    Loads a PEM-encoded public key from a file.

    Args:
        path (str): The file path to the public key.

    Returns:
        The public key object from the cryptography library.
    """
    data = Path(path).read_bytes()
    return serialization.load_pem_public_key(data)


# --- Core Cryptographic Operations ---

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """
    Decrypts a base64-encoded seed using the provided private key.
    Uses the RSA/OAEP algorithm with SHA-256, as specified by the task.

    Args:
        encrypted_seed_b64 (str): The base64-encoded encrypted seed.
        private_key: The private key object to use for decryption.

    Returns:
        The decrypted 64-character hexadecimal seed as a string.
    """
    ciphertext = base64.b64decode(encrypted_seed_b64)

    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    # Decode the decrypted bytes and validate the seed's format for robustness.
    hex_seed = plaintext.decode("utf-8").strip()
    if len(hex_seed) != 64:
        raise ValueError("Decrypted seed must be 64 hex characters long")
    if not all(c in "0123456789abcdef" for c in hex_seed):
        raise ValueError("Decrypted seed contains non-hex characters")

    return hex_seed


# --- Functions for the Final Commit Proof ---

def sign_message(message: str, private_key) -> bytes:
    """
    Signs a string message using the provided private key.
    Uses the RSA-PSS algorithm with SHA-256, as specified by the task.

    Args:
        message (str): The string to sign (e.g., a commit hash).
        private_key: The private key object to use for signing.

    Returns:
        The raw signature as bytes.
    """
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
    """
    Encrypts raw bytes using the provided public key.
    Uses the RSA/OAEP algorithm with SHA-256, as specified by the task.

    Args:
        data (bytes): The raw bytes to encrypt (e.g., a signature).
        public_key: The public key object to use for encryption.

    Returns:
        The encrypted ciphertext as bytes.
    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return ciphertext