import subprocess
import time

steps = [
    ("Ingestion", ["python", "-m", "ingestion.run_ingestion"]),
    ("Validation Clickstream", ["python", "-m", "validation.validate_clickstream"]),
    ("Validation Purchase", ["python", "-m", "validation.validate_purchase"]),
    ("Validation Products", ["python", "-m", "validation.validate_products"]),
    ("Prepare Data", ["python", "-m", "preprocessing.prepare_data"]),
    ("Feature Engineering", ["python", "-m", "transformation.feature_engineering"]),
    ("Register Feature Store", ["python", "-m", "feature_store.register_features"]),
    ("Prepare Training Data", ["python", "-m", "models.prepare_training_data"]),
    ("Train Model", ["python", "-m", "models.train_model"]),
    ("Evaluate Model", ["python", "-m", "models.evaluate"]),
]

for name, cmd in steps:
    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")

    start = time.time()

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print(f"FAILED: {name}")
        break

    print(f"Completed in {time.time()-start:.2f} sec")

print("\nPipeline Completed")