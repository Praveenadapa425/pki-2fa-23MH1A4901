# File: app/main.py (with debug endpoint)

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from pathlib import Path
import traceback  # Import the traceback module

# --- Correct Imports for a Packaged App ---
from .crypto_utils import load_private_key, decrypt_seed
from .totp_utils import generate_totp_code, verify_totp_code, seconds_remaining_in_period
from .config import SEED_FILE, DATA_DIR

app = FastAPI(title="PKI 2FA Microservice")

class DecryptSeedRequest(BaseModel):
    encrypted_seed: str

class Verify2FARequest(BaseModel):
    code: str | None = None

def get_hex_seed() -> str:
    if not SEED_FILE.exists():
        raise HTTPException(status_code=500, detail="Seed not decrypted yet.")
    try:
        return SEED_FILE.read_text(encoding="utf-8").strip()
    except Exception:
        raise HTTPException(status_code=500, detail="Error reading seed file.")

@app.on_event("startup")
def on_startup():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# --- START OF NEW DEBUG ENDPOINT ---
@app.post("/debug-decryption")
def debug_decryption_endpoint(body: DecryptSeedRequest):
    """
    A temporary endpoint to get detailed information about the decryption failure.
    """
    debug_info = {}
    try:
        # 1. Try to load the private key
        private_key = load_private_key("student_private.pem")
        debug_info["key_loading_status"] = "Success"

        # 2. Try to decrypt the seed and catch the specific error
        try:
            hex_seed = decrypt_seed(body.encrypted_seed, private_key)
            debug_info["decryption_status"] = "Success"
            debug_info["decrypted_seed_preview"] = hex_seed[:4] + "..."
        except Exception as e:
            debug_info["decryption_status"] = "Failed"
            # Get the exact cryptographic error message
            debug_info["decryption_error_type"] = type(e).__name__
            debug_info["decryption_error_message"] = str(e)
            debug_info["full_traceback"] = traceback.format_exc()
    except Exception as e:
        debug_info["key_loading_status"] = "Failed"
        debug_info["key_loading_error"] = str(e)

    return debug_info
# --- END OF NEW DEBUG ENDPOINT ---

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/decrypt-seed")
def decrypt_seed_endpoint(body: DecryptSeedRequest):
    try:
        private_key = load_private_key("student_private.pem")
        hex_seed = decrypt_seed(body.encrypted_seed, private_key)
        SEED_FILE.write_text(hex_seed, encoding="utf-8")
    except Exception:
        raise HTTPException(status_code=500, detail="Decryption failed")
    return {"status": "ok"}

@app.get("/generate-2fa")
def generate_2fa_endpoint():
    hex_seed = get_hex_seed()
    code = generate_totp_code(hex_seed)
    valid_for = seconds_remaining_in_period(30)
    return {"code": code, "valid_for": valid_for}

@app.post("/verify-2fa")
def verify_2fa_endpoint(body: Verify2FARequest):
    if body.code is None or not body.code.strip():
        raise HTTPException(status_code=400, detail="Missing code")
    hex_seed = get_hex_seed()
    is_valid = verify_totp_code(hex_seed, body.code, valid_window=1)
    return {"valid": is_valid}