from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd

MODEL_PATH = Path("models/saved_models/knn_model.pkl")


def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    saved = joblib.load(MODEL_PATH)
    return saved["model"], saved["matrix"]


def predict_top_k(user_id, top_k=5):
    model, matrix = load_model()

    if user_id not in matrix.index:
        raise KeyError(f"User {user_id} not found in training data")

    user_vector = matrix.loc[user_id].values.reshape(1, -1)
    distances, indices = model.kneighbors(user_vector, n_neighbors=min(top_k + 1, len(matrix.index)))

    similar_users = [matrix.index[i] for i in indices[0][1:]]
    similar_scores = [1 - dist for dist in distances[0][1:]]

    return {
        "user_id": user_id,
        "top_similar_users": similar_users,
        "similarity_scores": similar_scores,
        "top_k": top_k,
    }


def recommend_products(user_id, top_k=5):
    result = predict_top_k(user_id, top_k=top_k)
    return json.dumps(result, indent=2)


if __name__ == "__main__":
    print(recommend_products(1, top_k=5))
