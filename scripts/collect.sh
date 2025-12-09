#!/bin/bash
# ==============================================================================
# Script: collect.sh
# Description:
#   Queries the API at http://0.0.0.0:5000 to retrieve sales data for graphics
#   card models: rtx3060, rtx3070, rtx3080, rtx3090, rx6700
#   Saves a timestamped CSV in data/raw/ and logs in logs/collect.logs
# ==============================================================================

echo "-------------Collecting sales data------------------"

# Create necessary directories
mkdir -p data/raw
mkdir -p logs

# Variables
API_URL="http://0.0.0.0:5000"
OUTPUT_FILE="data/raw/sales_$(date -d '+1 hour' +%Y%m%d_%H%M).csv"
LOG_FILE="logs/collect.logs"
MODELS=("rtx3060" "rtx3070" "rtx3080" "rtx3090" "rx6700")

# Initialize output file with header
echo "timestamp,model,sales" > "$OUTPUT_FILE"

# Logging function
log_message() {
    echo "[$(date -d '+1 hour' '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Collect data for each model
for MODEL in "${MODELS[@]}"; do

    RESPONSE=$(curl -s "$API_URL/$MODEL")
    TIMESTAMP=$(date -d '+1 hour' '+%Y-%m-%d %H:%M:%S')
    echo "$TIMESTAMP,$MODEL,$RESPONSE" >> "$OUTPUT_FILE"
    log_message "INFO: Retrieved sales data for model $MODEL: $RESPONSE"

done

# Completion message
echo "Data collection complete. Output saved to $OUTPUT_FILE"
echo "Logs saved to $LOG_FILE"
echo "-----------------------------------------------------"
