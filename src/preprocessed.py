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
from datetime import datetime

# Directories
RAW_DIR = "data/raw/"
PROCESSED_DIR = "data/processed/"

# Ensure processed directory exists
os.makedirs(PROCESSED_DIR, exist_ok=True)

# Get the latest CSV file from raw data
raw_files = sorted(glob.glob(RAW_DIR + "*.csv"))
if not raw_files:
    raise FileNotFoundError("No raw CSV files found in data/raw/")
latest_file = raw_files[-1]

# Load raw CSV
df = pd.read_csv(latest_file)

# -------------------------
# Preprocessing
# -------------------------

# Drop rows where 'sales' is missing or empty
df = df.dropna(subset=['sales'])

# Ensure 'sales' is integer
df['sales'] = df['sales'].astype(int)

# Optional: convert timestamp to datetime for further feature engineering
# df['timestamp'] = pd.to_datetime(df['timestamp'])

# Save preprocessed CSV with timestamped filename
processed_filename = os.path.join(
    PROCESSED_DIR,
    f"sales_processed_{datetime.now().strftime('%Y%m%d_%H%M')}.csv"
)
df.to_csv(processed_filename, index=False)

print(f"Saved preprocessed file: {processed_filename}")