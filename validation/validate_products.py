import json
from pathlib import Path
import pandas as pd

RAW_DIR = Path("data/raw/products")

latest_file = sorted(RAW_DIR.glob("*.json"))[-1]

with open(latest_file) as f:
    products = json.load(f)

df = pd.DataFrame(products)

print("\nPRODUCT DATA QUALITY\n")

rows = len(df)
columns = len(df.columns)
missing_values = df.isnull().sum().sum()
duplicate_rows = df["id"].duplicated().sum()
invalid_price = (df["price"] <= 0).sum()

print(f"Rows : {rows}")
print(f"Columns : {columns}")
print(f"Missing Values : {missing_values}")
print(f"Duplicate Rows : {duplicate_rows}")
print(f"Invalid Price : {invalid_price}")

# -------------------------------
# Dynamic Validation Status
# -------------------------------
status = "Passed"

if (
    missing_values > 0
    or duplicate_rows > 0
    or invalid_price > 0
):
    status = "Failed"

print(f"\nValidation Status : {status}")

# Used by report_generator.py
VALIDATION_RESULT = {
    "Dataset": "Products",
    "Status": status,
    "Rows": rows,
    "Missing": missing_values,
    "Duplicates": duplicate_rows
}