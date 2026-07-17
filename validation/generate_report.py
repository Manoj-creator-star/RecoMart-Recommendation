import pandas as pd
from pathlib import Path
from datetime import datetime

from validation.validate_purchase import VALIDATION_RESULT as purchase
from validation.validate_clickstream import VALIDATION_RESULT as clickstream
from validation.validate_products import VALIDATION_RESULT as products

reports = [purchase, clickstream, products]

report = pd.DataFrame(reports)
report["Validation Time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

BASE_DIR = Path(__file__).resolve().parent.parent
REPORT_DIR = BASE_DIR / "validation_reports"
REPORT_DIR.mkdir(exist_ok=True)
REPORT_PATH = REPORT_DIR / "data_quality_report.csv"

report.to_csv(REPORT_PATH, index=False)

print("\n" + "=" * 65)
print("           RECOMART DATA QUALITY REPORT")
print("=" * 65)
print(f"Generated On : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

print(report.to_string(index=False))

print("\n" + "-" * 65)
print(f"Overall Status : {'PASSED' if (report['Status'] == 'Passed').all() else 'FAILED'}")
print(f"Datasets Checked : {len(report)}")
print(f"Passed : {(report['Status'] == 'Passed').sum()}")
print(f"Failed : {(report['Status'] == 'Failed').sum()}")
print("-" * 65)

print(f"\nCSV Report saved to {REPORT_PATH}")
print("=" * 65)