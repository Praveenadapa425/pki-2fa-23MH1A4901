# File: app/main.py (Final, Clean Version)

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pathlib import Path

# --- Correct Imports for Direct Execution ---
try:
    from .crypto_utils import load_private_key, decrypt_seed
    from .totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period
    from .config import SEED_FILE, DATA_DIR
except ImportError:
    from crypto_utils import load_private_key, decrypt_seed
    from totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period
    from config import SEED_FILE, DATA_DIR

app = FastAPI(title="PKI 2FA Microservice")

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str | None = None

def get_hex_seed() -> str:
    """Safely reads the decrypted hex seed from the persistent volume."""
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet.")
    try:
        hex_seed = SEED_FILE.read_text(encoding="utf-8").strip()
        # Validate that the hex seed is 64 characters and contains only hex characters
        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed):
            raise ValueError("Invalid seed format")
        return hex_seed
    except Exception:
        raise HTTPException(status_code=500, detail="Error reading seed file.")

@app.on_event("startup")
def on_startup():
    """Ensure the data directory exists when the application starts."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)

@app.get("/health")
def health_check():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok"}

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: DecryptSeedRequest):
    """Decrypts the provided seed and saves it to the persistent volume."""
    try:
        # Ensure the data directory exists
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        
        private_key = load_private_key("student_private.pem")
        hex_seed = decrypt_seed(body.encrypted_seed, private_key)
        
        # Validate that the hex seed is 64 characters and contains only hex characters
        if len(hex_seed) != 64 or not all(c in "0123456789abcdef" for c in hex_seed):
            raise ValueError("Invalid seed format")
        
        SEED_FILE.write_text(hex_seed, encoding="utf-8")
    except Exception as e:
        print(f"Decryption error: {e}")  # Log for debugging
        raise HTTPException(status_code=500, detail="Decryption failed")
    return {"status": "ok"}

@app.get("/generate-2fa")
def generate_2fa_endpoint():
    """Generates a new 2FA code."""
    hex_seed = get_hex_seed()
    code = generate_totp_code(hex_seed)
    valid_for = seconds_remaining_in_period(30)
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa_endpoint(body: Verify2FARequest):
    """Verifies a provided 2FA code."""
    if body.code is None or not body.code.strip():
        raise HTTPException(status_code=400, detail="Missing code")
    hex_seed = get_hex_seed()
    is_valid = verify_totp_code(hex_seed, body.code, valid_window=1)
    return {"valid": is_valid}