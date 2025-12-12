"""
-------------------------------------------------------------------------------
Script: train.py
Description:
    Trains an XGBoost model on the latest preprocessed sales data.
    Saves the model in 'model/' and logs metrics.

Steps:
1. Searches for the latest preprocessed CSV in 'data/processed/'.
2. Loads the data, encodes features, splits into train/test.
3. Trains an XGBoost model.
4. Evaluates RMSE, MAE, R² metrics.
5. Saves model in 'model/' folder as model.pkl or model_YYYYMMDD_HHMM.pkl.
-------------------------------------------------------------------------------
"""
import os
import glob
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import pickle
from datetime import datetime

# -----------------------------
# Directories
# -----------------------------
PROCESSED_DIR = "data/processed"
MODEL_DIR = "model"
os.makedirs(MODEL_DIR, exist_ok=True)

# -----------------------------
# Find latest preprocessed CSV
# -----------------------------
csv_files = sorted(glob.glob(os.path.join(PROCESSED_DIR, "sales_processed_*.csv")))
if not csv_files:
    raise FileNotFoundError(f"No preprocessed CSV files found in {PROCESSED_DIR}")
latest_file = csv_files[-1]
print(f"Using latest preprocessed file: {latest_file}")

# -----------------------------
# Load data
# -----------------------------
df = pd.read_csv(latest_file)

# -----------------------------
# Prepare features and target
# -----------------------------
# Features: one-hot encode 'model'
X = pd.get_dummies(df["model"])
y = df["sales"]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Determine model filename
# -----------------------------
standard_model_path = os.path.join(MODEL_DIR, "model.pkl")
timestamp = datetime.now().strftime("%Y%m%d_%H%M")
if os.path.exists(standard_model_path):
    model_path = os.path.join(MODEL_DIR, f"model_{timestamp}.pkl")
else:
    model_path = standard_model_path

# -----------------------------
# Train XGBoost regressor
# -----------------------------
model = xgb.XGBRegressor(
    objective='reg:squarederror',
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)
model.fit(X_train, y_train)

# -----------------------------
# Evaluate model
# -----------------------------
y_pred = model.predict(X_test)
# Manual RMSE calculation for compatibility
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.2f}, MAE: {mae:.2f}, R2: {r2:.2f}")

# -----------------------------
# Save model
# -----------------------------
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"Model saved to {model_path}")
