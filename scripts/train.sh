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

log_message "Starting model training"

# Activate environment
source .venv/bin/activate >> "$LOG_FILE" 2>&1

# Run Python training script
uv run python src/train.py >> "$LOG_FILE" 2>&1

log_message "Training completed"

echo "-------------------------------------------------------"
echo "Training complete. Logs saved to $LOG_FILE"
echo "-------------------------------------------------------"
