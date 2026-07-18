from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score

MODEL_PATH = Path("models/saved_models/knn_model.pkl")
TRAINING_FILE = Path("data/model/training_data.csv")
TOP_K_VALUES = [5, 10, 20]
SEED = 42


def load_model_and_matrix():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    saved = joblib.load(MODEL_PATH)
    return saved["model"], saved["matrix"]


def build_holdout_sample(matrix):
    rng = np.random.default_rng(SEED)
    sample = []
    for user_id in matrix.index:
        row = matrix.loc[user_id].values
        positive_items = np.where(row > 0)[0]
        if len(positive_items) > 1:
            held_out = rng.choice(positive_items)
            sample.append((user_id, held_out))
    return sample


def recommend_items(model, matrix, user_id, held_out_index, top_k):
    row = matrix.loc[user_id].values.astype(float).copy()
    row[held_out_index] = 0.0

    n_neighbors = min(model.n_neighbors + 1, matrix.shape[0])
    distances, neighbors = model.kneighbors(row.reshape(1, -1), n_neighbors=n_neighbors)
    distances, neighbors = distances[0], neighbors[0]

    user_pos = matrix.index.get_loc(user_id)
    keep = neighbors != user_pos
    distances = distances[keep]
    neighbors = neighbors[keep]

    similarities = np.clip(1 - distances, a_min=0, a_max=None)
    if similarities.sum() == 0:
        scores = np.zeros(matrix.shape[1])
    else:
        neighbor_matrix = matrix.iloc[neighbors].values.astype(float)
        scores = neighbor_matrix.T.dot(similarities) / similarities.sum()

    seen_mask = matrix.loc[user_id].values > 0
    scores[seen_mask] = -np.inf

    return np.argsort(scores)[::-1][:top_k]


def dcg_at_k(recommended_indices, relevant_index, k):
    for idx, item_index in enumerate(recommended_indices[:k]):
        if item_index == relevant_index:
            return 1.0 / np.log2(idx + 2)
    return 0.0


def ndcg_at_k(recommended_indices, relevant_index, k):
    ideal_dcg = 1.0
    if ideal_dcg == 0:
        return 0.0
    return dcg_at_k(recommended_indices, relevant_index, k) / ideal_dcg


def evaluate_top_k(model, matrix, sample, top_k):
    hits = []
    ndcgs = []

    for user_id, held_out_index in sample:
        recommended = recommend_items(model, matrix, user_id, held_out_index, top_k=top_k)
        hit = 1 if held_out_index in recommended else 0
        hits.append(hit)
        ndcgs.append(ndcg_at_k(recommended, held_out_index, top_k))

    total_hits = sum(hits)
    total_users = len(sample)

    precision = total_hits / (total_users * top_k) if total_users else 0.0
    recall = total_hits / total_users if total_users else 0.0
    f1 = (2 * precision * recall / (precision + recall)) if precision + recall > 0 else 0.0

    return {
        "top_k": top_k,
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1),
        "ndcg": float(np.mean(ndcgs)) if ndcgs else 0.0,
        "hit_rate": float(recall),
        "total_hits": int(total_hits),
    }


def compute_recommendation_metrics():
    ratings = pd.read_csv(TRAINING_FILE)
    model, matrix = load_model_and_matrix()

    sample = build_holdout_sample(matrix)
    results = {
        k: evaluate_top_k(model, matrix, sample, k)
        for k in TOP_K_VALUES
    }

    distances, _ = model.kneighbors(matrix)
    average_similarity = 1 - np.mean(distances)

    metrics = {
        "average_similarity": float(average_similarity),
        "users": int(matrix.shape[0]),
        "products": int(matrix.shape[1]),
        "holdout_samples": len(sample),
        "results": results,
    }

    return metrics


if __name__ == "__main__":
    print(json.dumps(compute_recommendation_metrics(), indent=2))
