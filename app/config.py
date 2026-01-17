# File: app/config.py

from pathlib import Path

# Define the paths for data storage inside the Docker container.
# Using Path objects makes handling file paths easier and more reliable.

# Use local directory when running outside Docker, /data when in container
import os

# Check if we're in a Docker container by looking for typical Docker indicators
in_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_ENV')

if in_docker and os.path.exists("/data") and os.access("/data", os.W_OK):
    DATA_DIR = Path("/data")
else:
    DATA_DIR = Path("./data")  # Fallback for local development

if in_docker and os.path.exists("/cron") and os.access("/cron", os.W_OK):
    CRON_DIR = Path("/cron")
else:
    CRON_DIR = Path("./cron_output")  # Fallback for local development

# Define the specific file path for the decrypted seed.
SEED_FILE = DATA_DIR / "seed.txt"