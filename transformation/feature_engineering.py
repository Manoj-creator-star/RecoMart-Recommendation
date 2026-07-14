import pandas as pd

from transformation.user_features import create_user_features
from transformation.product_features import create_product_features
from transformation.interaction_features import create_interaction_features
from transformation.load_to_sqlite import load_tables


df = pd.read_csv("data/processed/prepared_dataset.csv")

user_features = create_user_features(df)

product_features = create_product_features(df)

interaction_features = create_interaction_features(df)

load_tables(
    user_features,
    product_features,
    interaction_features
)

print("\nFeature Engineering Completed Successfully")

print("\nUser Features")
print(user_features.head())

print("\nProduct Features")
print(product_features.head())

print("\nInteraction Features")
print(interaction_features.head())