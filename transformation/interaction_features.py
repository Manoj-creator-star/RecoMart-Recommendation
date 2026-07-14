import pandas as pd

EVENT_SCORE = {
    "view": 1,
    "click": 2,
    "wishlist": 3,
    "add_to_cart": 4,
    "purchase": 5
}


def create_interaction_features(df):

    interaction = df[
        ["user_id", "product_id", "event"]
    ].copy()

    interaction["interaction_score"] = (
        interaction["event"]
        .map(EVENT_SCORE)
        .fillna(0)
    )

    return interaction