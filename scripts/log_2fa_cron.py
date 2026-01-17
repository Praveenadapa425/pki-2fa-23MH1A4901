# File: scripts/log_2fa_cron.py (Final, Corrected Version)

import sys
from pathlib import Path
from datetime import datetime, timezone
import time
import os # <-- Import the 'os' module to check for the file

# Add the parent directory (your project root) to the Python path.
sys.path.append(str(Path(__file__).resolve().parent.parent))

# --- START OF THE FIX ---
# The 'generate_totp_code' function lives in 'totp_utils', not 'crypto_utils'.
from app.totp_utils import generate_totp_code
# --- END OF THE FIX ---

# We get the file paths from the central config file
from app.config import SEED_FILE, CRON_DIR

def main():
    """Logs the current 2FA code to the cron output file."""
    log_path = CRON_DIR / "last_code.txt"
    try:
        if not SEED_FILE.exists():
            # If the seed hasn't been decrypted yet, do nothing.
            return

        hex_seed = SEED_FILE.read_text(encoding="utf-8").strip()
        # Validate that the hex seed is 64 characters and contains only hex characters
        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed):
            print(f"Invalid seed format in {SEED_FILE}", file=sys.stderr)
            return
        code = generate_totp_code(hex_seed)
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"{timestamp} - 2FA Code: {code}\n"
        
        # Append the new code to the log file.
        with open(log_path, "a") as log_file:
            log_file.write(log_entry)

    except Exception as e:
        # If a real error happens, print it to stderr for debugging.
        print(f"Error in cron script: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()