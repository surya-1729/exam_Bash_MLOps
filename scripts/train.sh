#!/bin/bash
# =============================================================================
# Script: train.sh
# Description:
#   Runs the train.py script in the active virtual environment
#   and logs output to logs/train.logs
# =============================================================================

LOG_FILE="logs/train.logs"

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

# Run the training script and log output
python src/train.py >> "$LOG_FILE" 2>&1

# Check exit status
if [ $? -eq 0 ]; then
    log_message "Script completed successfully"
else
    log_message "Script failed with exit code $?"
fi

# Completion message
echo "Model training complete. Logs saved to $LOG_FILE"
echo "-------------------------------------------------------"