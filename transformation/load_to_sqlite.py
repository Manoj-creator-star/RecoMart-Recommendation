import sqlite3
from pathlib import Path

DATABASE = Path("database")
DATABASE.mkdir(exist_ok=True)

DB_FILE = DATABASE / "feature_store.db"


def load_tables(user_df, product_df, interaction_df):

    conn = sqlite3.connect(DB_FILE)

    user_df.to_sql(
        "user_features",
        conn,
        if_exists="replace",
        index=False
    )

    product_df.to_sql(
        "product_features",
        conn,
        if_exists="replace",
        index=False
    )

    interaction_df.to_sql(
        "interaction_features",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

    print("SQLite Feature Store Created Successfully")