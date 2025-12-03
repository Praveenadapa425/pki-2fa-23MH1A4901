#!/usr/bin/env python3
import sys
from pathlib import Path
from datetime import datetime, timezone

# --- This is a crucial fix for imports ---
# When this script runs from cron, it doesn't know where the 'app' module is.
# This line adds your project's root directory to Python's path,
# allowing it to find and import from the 'app' folder.
sys.path.append(str(Path(__file__).resolve().parent.parent))
# --- End of fix ---

from app.crypto_utils import generate_totp_code

SEED_PATH = "/data/seed.txt"
LOG_PATH = "/cron/last_code.txt"

def main():
    """Reads the seed, generates a TOTP code, and logs it with a UTC timestamp."""
    try:
        if not os.path.exists(SEED_PATH):
            # If the seed hasn't been decrypted yet, do nothing.
            # This prevents filling the log with errors before setup.
            return

        with open(SEED_PATH, "r") as f:
            hex_seed = f.read().strip()
        
        code = generate_totp_code(hex_seed)
        timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        
        log_entry = f"{timestamp} - 2FA Code: {code}\n"
        
        # Append the new code to the log file.
        with open(LOG_PATH, "a") as log_file:
            log_file.write(log_entry)

    except Exception as e:
        # If a real error happens, print it to stderr for debugging.
        print(f"Error in cron script: {e}", file=sys.stderr)

if __name__ == "__main__":
    main()