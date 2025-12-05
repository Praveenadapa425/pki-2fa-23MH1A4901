import base64
import sys
from pathlib import Path
import subprocess  # To run Git commands

# Add the project root to the Python path to allow importing from the 'app' package
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.crypto_utils import load_private_key, load_public_key, sign_message, encrypt_with_public_key

def main():
    """
    Generates the encrypted commit proof required for submission.
    It automatically finds the latest commit hash.
    """
    try:
        # 1. Automatically get the latest commit hash from Git
        commit_hash = subprocess.check_output(
            ['git', 'log', '-1', '--format=%H']
        ).decode('utf-8').strip()
        print(f"Found latest commit hash: {commit_hash}")

        # 2. Load the necessary cryptographic keys
        print("\nLoading keys...")
        private_key = load_private_key("student_private.pem")
        instructor_pub = load_public_key("instructor_public.pem")
        print("Keys loaded successfully.")

        # 3. Sign the commit hash with your private key
        print("Signing commit hash with student private key...")
        signature = sign_message(commit_hash, private_key)
        
        # 4. Encrypt the resulting signature with the instructor's public key
        print("Encrypting signature with instructor public key...")
        encrypted_sig = encrypt_with_public_key(signature, instructor_pub)

        # 5. Base64 encode the final ciphertext for easy copying
        b64_encoded_sig = base64.b64encode(encrypted_sig).decode("utf-8")
        
        # 6. Print the final results for submission
        print("\n" + "="*60)
        print("✅ Submission Artifacts Generated Successfully")
        print("="*60)
        print(f"Commit Hash: {commit_hash}")
        print("\nEncrypted Commit Signature (copy the entire line below):")
        print(b64_encoded_sig)
        print("="*60)

    except FileNotFoundError as e:
        print(f"\n❌ ERROR: A required file was not found: {e.filename}")
        print("Please ensure 'student_private.pem' and 'instructor_public.pem' are in the project root.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()