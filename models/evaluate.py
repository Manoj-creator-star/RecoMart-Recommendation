from pathlib import Path

import joblib
import numpy as np

MODEL_PATH = Path("models/saved_models/knn_model.pkl")

saved = joblib.load(MODEL_PATH)

model = saved["model"]
matrix = saved["matrix"]

# =====================================================
# Simple Evaluation
# =====================================================

distances, indices = model.kneighbors(matrix)

average_similarity = 1 - np.mean(distances)

print("=" * 60)
print("MODEL EVALUATION")
print("=" * 60)

print(f"Users Evaluated : {matrix.shape[0]}")
print(f"Products        : {matrix.shape[1]}")
print(f"Average Similarity : {average_similarity:.4f}")

print("\nEvaluation Completed Successfully")