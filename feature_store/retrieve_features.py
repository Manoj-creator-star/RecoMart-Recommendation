import sqlite3
import pandas as pd

DATABASE = "database/feature_store.db"

conn = sqlite3.connect(DATABASE)


def get_user_features(user_id):

    query = f"""
    SELECT * FROM user_features
    WHERE user_id={user_id}
    """
    return pd.read_sql(query, conn)


def get_product_features(product_id):
    query = f"""
    SELECT * FROM product_features
    WHERE product_id={product_id}
    """
    return pd.read_sql(query, conn)


print("\n")
print(get_user_features(1))
print("\n")
print(get_product_features(5))
conn.close()