# PKI-Based 2FA Microservice

This project is a secure, containerized microservice that implements two-factor authentication using Public Key Infrastructure (PKI) and Time-based One-Time Passwords (TOTP), built with Python and FastAPI.

## Technology Stack
- **Language:** Python 3.11
- **API Framework:** FastAPI
- **Containerization:** Docker & Docker Compose
- **Cryptography:** `cryptography` library for RSA operations
- **TOTP:** `pyotp` library

## Core Features
- **PKI Operations:** Handles RSA 4096-bit key generation, RSA/OAEP decryption, and RSA-PSS signing.
- **Secure Seed Decryption:** A dedicated API endpoint (`/decrypt-seed`) to securely receive and persist the TOTP secret.
- **TOTP Functionality:** API endpoints to generate (`/generate-2fa`) and verify (`/verify-2fa`) standard 6-digit, 30-second TOTP codes.
- **Automated Background Task:** A `cron` job runs every minute inside the container to log the current 2FA code.
- **Persistent Storage:** Utilizes Docker Volumes to ensure the decrypted seed and cron logs survive container restarts.
- **Optimized Build:** A multi-stage `Dockerfile` creates a small and secure final container image.

## How to Run the Service

### Prerequisites
- Docker Desktop must be installed and running on your system.
- You must have a valid `encrypted_seed.txt` file in the project root, obtained from the instructor API.

### 1. Build the Docker Image
From the project's root directory, run the build command. This will create the container image based on the `Dockerfile`.
```bash
docker-compose build