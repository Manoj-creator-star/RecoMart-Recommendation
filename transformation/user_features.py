import pandas as pd


def create_user_features(df):

    user_features = (
        df.groupby("user_id")
        .agg(
            total_purchases=("order_id", "count"),
            total_quantity=("quantity", "sum"),
            avg_purchase_value=("price_x", "mean"),
            unique_products=("product_id", "nunique"),
        )
        .reset_index()
    )

    return user_features