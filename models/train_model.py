from pathlib import Path

import joblib
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# =====================================================
# Paths
# =====================================================

TRAINING_FILE = "data/model/training_data.csv"

MODEL_DIR = Path("models/saved_models")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = MODEL_DIR / "knn_model.pkl"

# =====================================================
# Load Training Data
# =====================================================

ratings = pd.read_csv(TRAINING_FILE)

print(f"Training Records : {len(ratings)}")

# =====================================================
# Create User-Item Matrix
# =====================================================

user_item_matrix = ratings.pivot_table(
    index="user_id",
    columns="product_id",
    values="rating",
    fill_value=0
)

# =====================================================
# Train Model
# =====================================================

model = NearestNeighbors(
    metric="cosine",
    algorithm="brute",
    n_neighbors=10
)

model.fit(user_item_matrix)

# =====================================================
# Save Model
# =====================================================

joblib.dump(
    {
        "model": model,
        "matrix": user_item_matrix
    },
    MODEL_PATH
)

print("=" * 60)
print("MODEL TRAINED SUCCESSFULLY")
print("=" * 60)
print(f"Users     : {user_item_matrix.shape[0]}")
print(f"Products  : {user_item_matrix.shape[1]}")
print(f"Model Saved : {MODEL_PATH}")