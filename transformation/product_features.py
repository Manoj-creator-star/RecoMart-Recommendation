import pandas as pd


def create_product_features(df):

    product_features = (
        df.groupby("product_id")
        .agg(
            category=("category", "first"),
            popularity=("order_id", "count"),
            avg_price=("price_x", "mean"),
            rating=("rating_rate", "mean"),
            rating_count=("rating_count", "mean"),
        )
        .reset_index()
    )

    return product_features