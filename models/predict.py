from pathlib import Path
import json
import joblib
import pandas as pd

MODEL_PATH = Path("models/saved_models/knn_model.pkl")
TRAINING_FILE = Path("data/model/training_data.csv")


def predict_for_user(user_id, top_n=5):
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    ratings = pd.read_csv(TRAINING_FILE)
    saved = joblib.load(MODEL_PATH)
    model = saved["model"]
    matrix = saved["matrix"]

    if user_id not in matrix.index:
        raise KeyError(f"User {user_id} not found in training data")

    user_vector = matrix.loc[user_id].values.reshape(1, -1)
    _, indices = model.kneighbors(user_vector, n_neighbors=min(top_n + 1, len(matrix.index)))

    similar_users = [int(matrix.index[i]) for i in indices[0][1:]]

    return {
        "user_id": int(user_id),
        "recommended_users": similar_users[:top_n],
    }


if __name__ == "__main__":
    print(json.dumps(predict_for_user(1, top_n=5), indent=2))
