# PKI-Based 2FA Microservice

This project is a secure, containerized microservice that implements two-factor authentication using Public Key Infrastructure (PKI) and Time-based One-Time Passwords (TOTP).

## Technology Stack
- **Language:** Python 3.11
- **API Framework:** FastAPI
- **Containerization:** Docker & Docker Compose
- **Cryptography:** `cryptography` library for RSA operations
- **TOTP:** `pyotp` library

## Features
- RSA 4096-bit key pair generation and usage.
- Secure seed decryption via an API endpoint.
- TOTP code generation and verification.
- Automated background task using `cron` to log 2FA codes every minute.
- Persistent data storage using Docker Volumes.
- Multi-stage Dockerfile for an optimized and secure final image.

## How to Run the Service

### Prerequisites
- Docker Desktop must be installed and running on your system.

### 1. Build the Docker Image
From the project's root directory, run the build command:
```bash
docker-compose build