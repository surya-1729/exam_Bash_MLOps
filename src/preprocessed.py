"""
-------------------------------------------------------------------------------
This script `preprocessed.py` retrieves data from the latest CSV file created 
in the 'data/raw/' directory.

1. It applies preprocessing to the data.
   
2. The results of the preprocessing are saved in a new CSV file 
   in the 'data/processed/' directory, with a name formatted as 
   'sales_processed_YYYYMMDD_HHMM.csv'.
   
3. All preprocessing steps are logged in the 
   'logs/preprocessed.logs' file to ensure detailed tracking of the process.

Any errors or anomalies are also logged to ensure traceability.
-------------------------------------------------------------------------------
"""
import pandas as pd
import glob
import os
from datetime import datetime, timedelta
import sys

# Setup logging
LOG_FILE = "logs/preprocessed.logs"

def log_message(message):
    """Log a message with timestamp"""
    timestamp = (datetime.now() + timedelta(hours=1)).strftime('%Y-%m-%d %H:%M:%S')
    log_line = f"[{timestamp}] {message}\n"
    
    # Ensure logs directory exists
    os.makedirs("logs", exist_ok=True)
    
    with open(LOG_FILE, "a") as f:
        f.write(log_line)
    
    print(message)

try:
    log_message("Starting preprocessing...")
    
    # Directories
    RAW_DIR = "data/raw/"
    PROCESSED_DIR = "data/processed/"
    
    # Ensure processed directory exists
    os.makedirs(PROCESSED_DIR, exist_ok=True)
    
    # Get the latest CSV file from raw data
    raw_files = sorted(glob.glob(RAW_DIR + "sales_*.csv"))
    if not raw_files:
        log_message("ERROR: No raw CSV files found in data/raw/")
        raise FileNotFoundError("No raw CSV files found in data/raw/")
    
    latest_file = raw_files[-1]
    log_message(f"Processing file: {latest_file}")
    
    # Load raw CSV
    df = pd.read_csv(latest_file)
    log_message(f"Loaded {len(df)} rows with columns: {list(df.columns)}")
    
    # -------------------------
    # Preprocessing
    # -------------------------
    
    # STEP 1: Drop the 'timestamp' column (REQUIRED by tests)
    if 'timestamp' in df.columns:
        df = df.drop('timestamp', axis=1)
        log_message("Dropped 'timestamp' column")
    
    # STEP 2: Drop rows where 'sales' is missing or empty
    df = df.dropna(subset=['sales'])
    log_message(f"After dropping NaN sales: {len(df)} rows")
    
    # STEP 3: Encode 'model' column as integer (REQUIRED by tests)
    if 'model' in df.columns:
        # Convert model names to categorical codes (0, 1, 2, ...)
        df['model'] = df['model'].astype('category').cat.codes
        log_message("Encoded 'model' column as integer")
    
    # STEP 4: Ensure all columns are integer type (REQUIRED by tests)
    for col in df.columns:
        if not pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].astype(int)
            log_message(f"Converted '{col}' to integer type")
    
    # Verify all columns are integers
    all_integer = all(pd.api.types.is_integer_dtype(df[col]) for col in df.columns)
    log_message(f"All columns are integer type: {all_integer}")
    
    if not all_integer:
        log_message("ERROR: Not all columns are integer type!")
        raise ValueError("Preprocessing failed: non-integer columns detected")
    
    # Final data info
    log_message(f"Final preprocessed data: {len(df)} rows, columns: {list(df.columns)}")
    log_message(f"Column types: {dict(df.dtypes)}")
    
    # -------------------------
    # Save Preprocessed Data
    # -------------------------
    
    # Save preprocessed CSV with timestamped filename
    processed_filename = os.path.join(
        PROCESSED_DIR,
        f"sales_processed_{(datetime.now() + timedelta(hours=1)).strftime('%Y%m%d_%H%M')}.csv"
    )
    df.to_csv(processed_filename, index=False)
    
    log_message(f"Saved preprocessed file: {processed_filename}")
    print(f"✓ Preprocessing complete: {processed_filename}")

except Exception as e:
    log_message(f"ERROR: {str(e)}")
    sys.exit(1)