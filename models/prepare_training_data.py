from pathlib import Path
import sqlite3
import pandas as pd

# Paths
DATABASE = "database/feature_store.db"

OUTPUT_DIR = Path("data/model")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "training_data.csv"

# Read interaction features
conn = sqlite3.connect(DATABASE)

df = pd.read_sql(
    """
    SELECT
        user_id,
        product_id,
        interaction_score AS rating
    FROM interaction_features
    """,
    conn,
)

conn.close()

# Remove duplicates
df = df.drop_duplicates()

# Save
df.to_csv(OUTPUT_FILE, index=False)

print("=" * 50)
print("Training Data Created Successfully")
print("=" * 50)

print(df.head())

print(f"\nRows    : {len(df)}")
print(f"Columns : {len(df.columns)}")

print(f"\nSaved To : {OUTPUT_FILE}")