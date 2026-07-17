from pathlib import Path
import json
import joblib
import numpy as np
import pandas as pd
from sklearn.neighbors import NearestNeighbors

ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = ROOT / "models" / "saved_models" / "knn_model.pkl"
K = 10
SEED = 42


def load_model_artifacts():
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model not found at {MODEL_PATH}")

    saved = joblib.load(MODEL_PATH)
    return saved["model"], saved["matrix"], saved.get("product_features")


def build_leave_one_out_sample(matrix, min_interactions=2, seed=SEED):
    rng = np.random.default_rng(seed)
    sample = []
    for user_row_idx in range(matrix.shape[0]):
        row = matrix.iloc[user_row_idx].values
        interacted_cols = np.where(row > 0)[0]
        if len(interacted_cols) < min_interactions:
            continue
        held_out_col = rng.choice(interacted_cols)
        sample.append((user_row_idx, held_out_col))
    return sample


def dcg_at_k(recommended, relevant, k=K):
    dcg = 0.0
    for i, item in enumerate(recommended[:k]):
        if item in relevant:
            dcg += 1 / np.log2(i + 2)
    return dcg


def ndcg_at_k(recommended, relevant, k=K):
    ideal_dcg = dcg_at_k(relevant, relevant, k)
    if ideal_dcg == 0:
        return 0.0
    return dcg_at_k(recommended, relevant, k) / ideal_dcg


def evaluate_ranking(sample, recommend_fn, k=K):
    precisions, recalls, ndcgs = [], [], []
    for user_row_idx, held_out_col in sample:
        relevant = [held_out_col]
        recommended = recommend_fn(user_row_idx, held_out_col, k)
        hit = held_out_col in recommended
        precisions.append((1 if hit else 0) / k)
        recalls.append(1 if hit else 0)
        ndcgs.append(ndcg_at_k(recommended, relevant, k))
    return {
        "users_evaluated": len(precisions),
        "precision_at_k": float(np.mean(precisions)) if precisions else 0.0,
        "recall_at_k": float(np.mean(recalls)) if recalls else 0.0,
        "ndcg_at_k": float(np.mean(ndcgs)) if ndcgs else 0.0,
    }


def recommend_user_based(user_row_idx, held_out_col_idx, matrix, knn_model, k=K):
    row = matrix.iloc[user_row_idx].values.astype(float).copy()
    row[held_out_col_idx] = 0.0

    n_neighbors = min(knn_model.n_neighbors + 1, matrix.shape[0])
    distances, neighbor_idx = knn_model.kneighbors(row.reshape(1, -1), n_neighbors=n_neighbors)
    distances, neighbor_idx = distances[0], neighbor_idx[0]

    keep = neighbor_idx != user_row_idx
    distances, neighbor_idx = distances[keep], neighbor_idx[keep]

    similarities = np.clip(1 - distances, a_min=0, a_max=None)
    if similarities.sum() == 0:
        neighbor_scores = np.zeros(matrix.shape[1])
    else:
        neighbor_matrix = matrix.iloc[neighbor_idx].values.astype(float)
        neighbor_scores = neighbor_matrix.T.dot(similarities) / similarities.sum()

    already_seen = row > 0
    neighbor_scores[already_seen] = -np.inf
    return np.argsort(neighbor_scores)[::-1][:k].tolist()


def recommend_item_based(user_row_idx, held_out_col_idx, matrix, item_knn_model, k=K):
    row = matrix.iloc[user_row_idx].values.astype(float).copy()
    row[held_out_col_idx] = 0.0
    interacted_items = np.where(row > 0)[0]

    if len(interacted_items) == 0:
        return []

    item_scores = np.zeros(matrix.shape[1])
    n_neighbors = min(item_knn_model.n_neighbors + 1, matrix.shape[1])

    for item_idx in interacted_items:
        item_vector = matrix.T.iloc[item_idx].values.astype(float).reshape(1, -1)
        distances, neighbor_items = item_knn_model.kneighbors(item_vector, n_neighbors=n_neighbors)
        distances, neighbor_items = distances[0], neighbor_items[0]
        similarities = np.clip(1 - distances, a_min=0, a_max=None)
        item_scores[neighbor_items] += similarities * row[item_idx]

    already_seen = row > 0
    item_scores[already_seen] = -np.inf
    return np.argsort(item_scores)[::-1][:k].tolist()


def recommend_popularity(user_row_idx, held_out_col_idx, matrix, popularity_rank, k=K):
    row = matrix.iloc[user_row_idx].values.astype(float).copy()
    row[held_out_col_idx] = 0.0
    already_seen = set(np.where(row > 0)[0].tolist())
    recommended = [item for item in popularity_rank if item not in already_seen]
    return recommended[:k]


def recommend_hybrid(user_row_idx, held_out_col_idx, matrix, knn_model, popularity_rank,
                      product_features=None, k=K, min_interactions_for_knn=5):
    row = matrix.iloc[user_row_idx].values
    n_interactions = (row > 0).sum()

    if n_interactions >= min_interactions_for_knn:
        return recommend_user_based(user_row_idx, held_out_col_idx, matrix, knn_model, k=k)

    already_seen = set(np.where(row > 0)[0].tolist()) - {held_out_col_idx}
    if product_features is not None and "rating" in product_features.columns:
        ranked = product_features.reindex(matrix.columns)["rating"].fillna(0)
        ranked_idx = np.argsort(ranked.values)[::-1]
        candidates = [i for i in ranked_idx if i not in already_seen]
    else:
        candidates = [i for i in popularity_rank if i not in already_seen]
    return candidates[:k]


def run_evaluation():
    model, matrix, product_features = load_model_artifacts()

    distances, _ = model.kneighbors(matrix)
    average_similarity = 1 - np.mean(distances)

    loo_sample = build_leave_one_out_sample(matrix, seed=SEED)

    item_totals = matrix.sum(axis=0)
    popularity_order = item_totals.sort_values(ascending=False).index
    popularity_rank = [matrix.columns.get_loc(c) for c in popularity_order]

    sweep_results = []
    for n in [5, 10, 15, 20, 30, 50]:
        n = min(n, matrix.shape[0] - 1)
        knn_sweep = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=n)
        knn_sweep.fit(matrix.values)
        metrics = evaluate_ranking(
            loo_sample,
            recommend_fn=lambda u, h, k, knn=knn_sweep: recommend_user_based(u, h, matrix, knn, k=k),
            k=K,
        )
        sweep_results.append({"n_neighbors": n, **metrics})

    item_knn_model = NearestNeighbors(metric="cosine", algorithm="brute", n_neighbors=min(20, matrix.shape[1] - 1))
    item_knn_model.fit(matrix.T.values)

    model_variants = {
        "Popularity Baseline": lambda u, h, k: recommend_popularity(u, h, matrix, popularity_rank, k=k),
        "User-based KNN (original)": lambda u, h, k: recommend_user_based(u, h, matrix, model, k=k),
        "Item-based KNN": lambda u, h, k: recommend_item_based(u, h, matrix, item_knn_model, k=k),
        "Hybrid (KNN + content fallback)": lambda u, h, k: recommend_hybrid(
            u, h, matrix, model, popularity_rank, product_features, k=k
        ),
    }

    all_results = {}
    for name, fn in model_variants.items():
        all_results[name] = evaluate_ranking(loo_sample, fn, k=K)

    best_model_name = max(all_results, key=lambda name: all_results[name]["ndcg_at_k"])
    metrics = {
        "average_similarity": float(average_similarity),
        "users": int(matrix.shape[0]),
        "products": int(matrix.shape[1]),
        "sweep_results": sweep_results,
        "comparison": all_results,
        "best_model": best_model_name,
    }
    return metrics


def main():
    metrics = run_evaluation()
    print("=" * 60)
    print("MODEL EVALUATION")
    print("=" * 60)
    print(f"Users Evaluated : {metrics['users']}")
    print(f"Products        : {metrics['products']}")
    print(f"Average Similarity : {metrics['average_similarity']:.4f}")
    print(f"Best Model : {metrics['best_model']}")
    print("\nEvaluation Completed Successfully")


if __name__ == "__main__":
    main()