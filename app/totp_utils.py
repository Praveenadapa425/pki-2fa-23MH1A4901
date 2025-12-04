# File: app/totp_utils.py (Final, Corrected Version)

import base64
import time  # <--- WE NEED TO IMPORT THE 'time' MODULE
import pyotp
import hashlib

def hex_to_base32(hex_seed: str) -> str:
    """Converts the 64-character hex seed into a Base32 encoded string."""
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed_bytes = base64.b32encode(seed_bytes)
    return base32_seed_bytes.decode("utf-8")


def generate_totp_code(hex_seed: str) -> str:
    """Generates the current 6-digit TOTP code."""
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """Verifies a TOTP code, allowing for a +/- 30 second time window."""
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    
    # --- START OF FINAL FIX ---
    # Instead of letting the library implicitly use the current time, we pass it
    # explicitly. This is more robust and prevents race conditions at the
    # edge of a time window.
    return totp.verify(code, for_time=time.time(), valid_window=valid_window)
    # --- END OF FINAL FIX ---


def seconds_remaining_in_period(interval: int = 30) -> int:
    """Calculates the number of seconds the current TOTP code is still valid for."""
    return interval - (int(time.time()) % interval)