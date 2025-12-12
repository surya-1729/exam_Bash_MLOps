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

    log_message "Querying model: $MODEL"
    RESPONSE=$(curl -s "$API_URL/$MODEL")
    TIMESTAMP=$(date -d '+1 hour' '+%Y-%m-%d %H:%M:%S')
    echo "$TIMESTAMP,$MODEL,$RESPONSE" >> "$OUTPUT_FILE"
    log_message "INFO: Retrieved sales data for model $MODEL: $RESPONSE"

done

# Verify file was created
if [ -f "$OUTPUT_FILE" ]; then
    line_count=$(wc -l < "$OUTPUT_FILE")
    log_message "Collection complete. File created with $line_count lines"
    log_message "=== Data collection finished ==="
else
    log_message "ERROR: Output file was not created"
    log_message "=== Data collection failed ==="
    exit 1
fi

echo "Data collection complete. Output: $OUTPUT_FILE"
