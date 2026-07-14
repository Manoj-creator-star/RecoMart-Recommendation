import sqlite3

DATABASE = "database/feature_store.db"

conn = sqlite3.connect(DATABASE)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS feature_metadata(

feature_name TEXT,

entity TEXT,

source_table TEXT,

transformation TEXT,

version TEXT

)
""")

metadata = [

("total_purchases",
"user",
"purchase_history",
"COUNT(order_id)",
"v1"),

("total_quantity",
"user",
"purchase_history",
"SUM(quantity)",
"v1"),

("avg_purchase_value",
"user",
"purchase_history",
"AVG(price_x)",
"v1"),

("unique_products",
"user",
"purchase_history",
"COUNT(DISTINCT product_id)",
"v1"),

("popularity",
"product",
"prepared_dataset",
"COUNT(order_id)",
"v1"),

("avg_price",
"product",
"prepared_dataset",
"AVG(price_x)",
"v1"),

("rating",
"product",
"Fake Store API",
"Average rating",
"v1"),

("interaction_score",
"interaction",
"clickstream",
"Weighted Event",
"v1")

]

cursor.executemany("""

INSERT INTO feature_metadata

VALUES(?,?,?,?,?)

""",metadata)

conn.commit()

conn.close()

print("Feature Metadata Registered Successfully")