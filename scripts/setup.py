import os
import requests
from dotenv import load_dotenv

# This loads the variables from your .env file
load_dotenv() 

def request_encrypted_seed():
    """Requests the encrypted seed from the instructor API and saves it."""
    api_url = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"
    student_id = os.getenv("STUDENT_ID")
    github_repo_url = os.getenv("GITHUB_REPO_URL")

    # --- Verification Step ---
    # Check that the .env file is filled out correctly.
    if not student_id or not github_repo_url:
        print("❌ ERROR: Please set STUDENT_ID and GITHUB_REPO_URL in the .env file.")
        return

    try:
        # --- Read the Public Key ---
        # Read your public key from the file to send it to the API.
        with open("student_public.pem", "r") as f:
            public_key_pem = f.read()

        # --- Prepare the Payload (This is the updated part) ---
        # The 'requests' library's json parameter handles the conversion of Python
        # objects to a valid JSON string automatically, including multi-line strings.
        # We should pass the raw PEM string directly without any manual formatting.
        payload = {
            "student_id": student_id,
            "github_repo_url": github_repo_url,
            "public_key": public_key_pem  # <-- Pass the raw key string directly
        }
        
        print("🚀 Requesting encrypted seed from instructor API...")
        
        # --- Make the API Call ---
        # Send the payload as JSON. 'requests' will format it correctly.
        response = requests.post(api_url, json=payload)
        
        # This will automatically raise an error for bad responses (like 4xx or 5xx)
        response.raise_for_status() 
        
        # --- Process the Response ---
        data = response.json()
        encrypted_seed = data.get("encrypted_seed")

        if encrypted_seed:
            # Save the received seed to the required file
            with open("encrypted_seed.txt", "w") as f:
                f.write(encrypted_seed)
            print("✅ Success! Your unique encrypted_seed.txt has been saved.")
        else:
            print("❌ ERROR: 'encrypted_seed' not found in API response.")
            print("API Response:", data)

    except FileNotFoundError:
        print("❌ ERROR: student_public.pem not found. Run crypto_utils.py first.")
    except requests.exceptions.RequestException as e:
        print(f"❌ ERROR: API request failed: {e}")

if __name__ == "__main__":
    request_encrypted_seed()