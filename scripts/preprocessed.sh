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

# Set PATH to include common binary locations
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin:$HOME/.local/bin:$PATH"

# Log script start
log_message "Script started"

# Sync project and activate virtual environment
uv sync >> "$LOG_FILE" 2>&1
source .venv/bin/activate >> "$LOG_FILE" 2>&1

# Run the preprocessing script and log output
python src/preprocessed.py >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    log_message "Script completed successfully"
else
    log_message "Script failed with exit code $?"
fi

# Completion message
echo "Preprocessing complete. Logs saved to $LOG_FILE"
echo "-------------------------------------------------------"