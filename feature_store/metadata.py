import sqlite3
import pandas as pd

conn = sqlite3.connect("database/feature_store.db")

df = pd.read_sql(

"SELECT * FROM feature_metadata",

conn

)

print(df)

conn.close()