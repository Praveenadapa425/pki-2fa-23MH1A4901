# --- Stage 1: The Builder ---
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- Stage 2: The Final Image ---
FROM python:3.11-slim
WORKDIR /app

# Set Timezone to UTC
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install cron
RUN apt-get update && apt-get install -y cron && rm -rf /var/lib/apt/lists/*

# Copy dependencies and executables from the builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy all your application code
COPY . .

# Create the cron file directly inside the Linux container using the FULL PATH to python3.
# This avoids all Windows formatting issues and all PATH environment issues.
RUN echo "* * * * * /usr/local/bin/python3 /app/scripts/log_2fa_cron.py >> /cron/last_code.txt 2>&1" > /etc/cron.d/2fa-cron

# Give the new file the correct permissions
RUN chmod 0644 /etc/cron.d/2fa-cron

# Apply the cron job from the newly created file
RUN crontab /etc/cron.d/2fa-cron

# Create the directories for our persistent data volumes
RUN mkdir -p /data /cron

# Expose the port
EXPOSE 8080

# The command to run when the container starts
# CRITICAL FIX: The host IP address has been corrected from '0.0.0.d' to '0.0.0.0'
CMD ["sh", "-c", "cron && uvicorn app.main:app --host 0.0.0.0 --port 8080"]