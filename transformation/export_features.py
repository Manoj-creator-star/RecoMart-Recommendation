import sqlite3
from pathlib import Path

import pandas as pd

DB = "database/feature_store.db"

OUTPUT = Path("feature_store/feature_repo/data")
OUTPUT.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB)

tables = [
    "user_features",
    "product_features",
    "interaction_features"
]

for table in tables:

    df = pd.read_sql(f"SELECT * FROM {table}", conn)

    df.to_csv(
        OUTPUT / f"{table}.csv",
        index=False
    )

    print(f"Exported {table}")

conn.close()