# File: app/config.py

from pathlib import Path

# Define the paths for data storage inside the Docker container.
# Using Path objects makes handling file paths easier and more reliable.

DATA_DIR = Path("/data")
CRON_DIR = Path("/cron")

# Define the specific file path for the decrypted seed.
SEED_FILE = DATA_DIR / "seed.txt"