#!/bin/bash
# =============================================================================
# This script preprocessed.sh runs the program src/preprocessed.py
# and logs the execution details in the log file
# logs/preprocessed.logs.
# =============================================================================

echo "-------------Preprocessing sales data------------------"

LOG_FILE="logs/preprocessed.logs"

# Logging function
log_message() {
    echo "[$(date -d '+1 hour' '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Make sure dependencies are installed (user-level, no venv)
python3 -m pip install --upgrade --user pip >> "$LOG_FILE" 2>&1
python3 -m pip install --user -r requirements.txt >> "$LOG_FILE" 2>&1

uv venv .venv >> "$LOG_FILE" 2>&1
source .venv/bin/activate >> "$LOG_FILE" 2>&1
uv add -r requirements.txt >> "$LOG_FILE" 2>&1

# Run the preprocessing script and log output
uv run which python >> "$LOG_FILE" 2>&1
uv run python src/preprocessed.py >> "$LOG_FILE" 2>&1

# Completion message
echo "Preprocessing complete. Logs saved to $LOG_FILE"
echo "-------------------------------------------------------" 
