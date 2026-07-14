import pandas as pd
from pathlib import Path

from validation.utils import validation_summary

RAW_DIR = Path("data/raw/purchase")

latest_file = sorted(RAW_DIR.glob("*.csv"))[-1]

df = pd.read_csv(latest_file)

summary = validation_summary(df)

print("\nPURCHASE DATA QUALITY\n")

for k, v in summary.items():
    print(f"{k}: {v}")

negative_price = (df["price"] < 0).sum()
negative_quantity = (df["quantity"] <= 0).sum()

print(f"\nNegative Price Records : {negative_price}")
print(f"Invalid Quantity Records : {negative_quantity}")

# -------------------------------
# Dynamic Validation Status
# -------------------------------
status = "Passed"

if (
    summary["Missing Values"] > 0
    or summary["Duplicate Rows"] > 0
    or negative_price > 0
    or negative_quantity > 0
):
    status = "Failed"

print(f"\nValidation Status : {status}")

# This can be imported by report_generator.py
VALIDATION_RESULT = {
    "Dataset": "Purchase",
    "Status": status,
    "Rows": len(df),
    "Missing": summary["Missing Values"],
    "Duplicates": summary["Duplicate Rows"]
}