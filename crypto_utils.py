from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair():
    """Generates a 4096-bit RSA key pair and saves it to PEM files."""
    print("Generating 4096-bit RSA key pair... This might take a moment.")
    
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    with open("student_private.pem", "wb") as f:
        f.write(private_pem)
    print("✅ Successfully saved student_private.pem")

    public_key = private_key.public_key()
    
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    with open("student_public.pem", "wb") as f:
        f.write(public_pem)
    print("✅ Successfully saved student_public.pem")

# This part allows us to run the function directly from the command line
if __name__ == "__main__":
    generate_rsa_keypair()