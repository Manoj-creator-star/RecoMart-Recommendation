import pandas as pd
from pathlib import Path

from validation.utils import validation_summary

RAW_DIR = Path("data/raw/clickstream")

latest_file = sorted(RAW_DIR.glob("*.csv"))[-1]

df = pd.read_csv(latest_file)

summary = validation_summary(df)

print("\nCLICKSTREAM DATA QUALITY\n")

for k, v in summary.items():
    print(f"{k}: {v}")

# Event validation
valid_events = [
    "view",
    "click",
    "wishlist",
    "add_to_cart"
]

invalid = df[~df["event"].isin(valid_events)]

print(f"\nInvalid Events : {len(invalid)}")

# -------------------------------
# Dynamic Validation Status
# -------------------------------
status = "Passed"

if (
    summary["Missing Values"] > 0
    or summary["Duplicate Rows"] > 0
    or len(invalid) > 0
):
    status = "Failed"

print(f"\nValidation Status : {status}")

# Used by report_generator.py
VALIDATION_RESULT = {
    "Dataset": "Clickstream",
    "Status": status,
    "Rows": len(df),
    "Missing": summary["Missing Values"],
    "Duplicates": summary["Duplicate Rows"]
}