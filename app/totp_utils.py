# File: app/totp_utils.py

import base64
import time
import pyotp
from cryptography.hazmat.primitives import hashes

def hex_to_base32(hex_seed: str) -> str:
    """Converts the 64-character hex seed into a Base32 encoded string."""
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed_bytes = base64.b32encode(seed_bytes)
    return base32_seed_bytes.decode("utf-8")


def generate_totp_code(hex_seed: str) -> str:
    """Generates the current 6-digit TOTP code."""
    base32_seed = hex_to_base32(hex_seed)
    # The task specifies SHA-1 for the TOTP algorithm
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashes.SHA1)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """Verifies a TOTP code, allowing for a +/- 30 second time window."""
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashes.SHA1)
    # valid_window=1 checks the current, previous, and next code periods.
    return totp.verify(code, valid_window=valid_window)


def seconds_remaining_in_period(interval: int = 30) -> int:
    """Calculates the number of seconds the current TOTP code is still valid for."""
    return interval - (int(time.time()) % interval)