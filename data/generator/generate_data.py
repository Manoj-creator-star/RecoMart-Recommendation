import random
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

# ------------------------
# Configuration
# ------------------------

NUM_USERS = 500
NUM_PRODUCTS = 20          # Fake Store API currently returns 20 products
NUM_CLICKSTREAM = 10000
NUM_PURCHASES = 2500

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DIR = BASE_DIR / "source"
SOURCE_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------
# Generate Clickstream
# ------------------------

events = [
    "view",
    "click",
    "wishlist",
    "add_to_cart"
]

clickstream = []

for _ in range(NUM_CLICKSTREAM):

    user = random.randint(1, NUM_USERS)

    product = random.randint(1, NUM_PRODUCTS)

    event = random.choices(
        events,
        weights=[55,25,10,10]
    )[0]

    timestamp = fake.date_time_between(
        start_date="-90d",
        end_date="now"
    )

    clickstream.append([
        user,
        product,
        event,
        timestamp
    ])

click_df = pd.DataFrame(
    clickstream,
    columns=[
        "user_id",
        "product_id",
        "event",
        "timestamp"
    ]
)

# ------------------------
# Generate Purchases
# ------------------------

purchase_rows = []

for order in range(1, NUM_PURCHASES + 1):

    quantity = random.randint(1,5)

    price = round(np.random.uniform(15,400),2)

    purchase_rows.append([

        order,

        random.randint(1,NUM_USERS),

        random.randint(1,NUM_PRODUCTS),

        quantity,

        price,

        fake.date_time_between(
            start_date="-90d",
            end_date="now"
        )

    ])

purchase_df = pd.DataFrame(

    purchase_rows,

    columns=[

        "order_id",

        "user_id",

        "product_id",

        "quantity",

        "price",

        "purchase_time"

    ]

)

# ------------------------
# Save
# ------------------------

click_df.to_csv(
    SOURCE_DIR / "clickstream.csv",
    index=False
)

purchase_df.to_csv(
    SOURCE_DIR / "purchase_history.csv",
    index=False
)

print("Generated Successfully!")
print(f"Clickstream Records : {len(click_df)}")
print(f"Purchase Records    : {len(purchase_df)}")