# File: app/totp_utils.py (with improved comments)

import base64
import time
import pyotp
import hashlib

def hex_to_base32(hex_seed: str) -> str:
    """
    Converts a 64-character hexadecimal seed into a Base32 encoded string.
    This is the required format for the pyotp library.

    Args:
        hex_seed (str): The 64-character hexadecimal seed.

    Returns:
        The Base32 encoded seed as a string.
    """
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed_bytes = base64.b32encode(seed_bytes)
    return base32_seed_bytes.decode("utf-8")


def generate_totp_code(hex_seed: str) -> str:
    """
    Generates the current 6-digit Time-based One-Time Password.

    Args:
        hex_seed (str): The 64-character hexadecimal seed.

    Returns:
        The current 6-digit TOTP code as a string.
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    return totp.now()


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Verifies a TOTP code, allowing for a time tolerance window.

    Args:
        hex_seed (str): The 64-character hexadecimal seed.
        code (str): The 6-digit code to verify.
        valid_window (int): The number of periods before/after to accept.
                            Default is 1 (accepts current, previous, and next code).

    Returns:
        True if the code is valid within the window, False otherwise.
    """
    base32_seed = hex_to_base32(hex_seed)
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    
    # Explicitly passing for_time makes the verification more robust and prevents
    # race conditions at the edge of a 30-second time window.
    return totp.verify(code, for_time=time.time(), valid_window=valid_window)


def seconds_remaining_in_period(interval: int = 30) -> int:
    """
    Calculates the number of seconds remaining in the current TOTP period.

    Args:
        interval (int): The TOTP time period in seconds. Defaults to 30.

    Returns:
        The number of seconds (0-29) left before the code changes.
    """
    return interval - (int(time.time()) % interval)