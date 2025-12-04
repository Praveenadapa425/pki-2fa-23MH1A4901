import os
import requests
from dotenv import load_dotenv
import sys
from pathlib import Path

# Add the project root to the path to allow importing from 'app'
sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.crypto_utils import decrypt_seed, load_private_key

# Load the variables from your .env file
load_dotenv() 

def request_encrypted_seed():
    # ... (this function remains the same as before) ...
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    student_id = os.getenv("STUDENT_ID")
    github_repo_url = os.getenv("GITHUB_REPO_URL")
    # ... etc ...

# --- START OF NEW DEBUG FUNCTION ---
def debug_local_decryption():
    """
    Performs the decryption locally to bypass any curl/shell issues.
    This provides a definitive test of the cryptographic functions.
    """
    print("\n--- Starting Local Decryption Debug ---")
    try:
        # 1. Load the private key
        private_key = load_private_key("student_private.pem")
        print("✅ Private key loaded successfully.")

        # 2. Read the encrypted seed from the file
        with open("encrypted_seed.txt", "r") as f:
            encrypted_seed_b64 = f.read().strip()
        print(f"✅ Encrypted seed loaded. Length: {len(encrypted_seed_b64)} characters.")

        # 3. Perform the decryption
        print("Attempting to decrypt...")
        decrypted_seed = decrypt_seed(encrypted_seed_b64, private_key)
        print("\n" + "="*50)
        print("✅✅✅ DECRYPTION SUCCEEDED! ✅✅✅")
        print("="*50)
        print(f"Decrypted Seed: {decrypted_seed}")
        print(f"Seed Length: {len(decrypted_seed)} characters (should be 64)")

    except Exception as e:
        print("\n" + "!"*50)
        print("❌❌❌ LOCAL DECRYPTION FAILED ❌❌❌")
        print("!"*50)
        print(f"Error Type: {type(e).__name__}")
        print(f"Error Message: {e}")
        import traceback
        traceback.print_exc()
# --- END OF NEW DEBUG FUNCTION ---

if __name__ == "__main__":
    # Use command-line arguments to choose the action
    if len(sys.argv) > 1 and sys.argv[1] == 'debug':
        debug_local_decryption()
    else:
        # This is the default action if you just run 'python scripts/setup.py'
        # request_encrypted_seed()
        print("Run 'python scripts/setup.py debug' to test local decryption.")