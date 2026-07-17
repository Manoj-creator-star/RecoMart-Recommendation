import subprocess
import time


def run_step(name, cmd):

    print(f"\n{'='*60}")
    print(f"Running: {name}")
    print(f"{'='*60}")

    start = time.time()

    result = subprocess.run(cmd)

    if result.returncode != 0:
        raise Exception(f"{name} Failed")

    print(f"Completed in {time.time()-start:.2f} sec")


def recomart_pipeline():

    run_step(
        "Ingestion",
        ["python", "-m", "ingestion.run_ingestion"]
    )

    run_step(
        "Validation Clickstream",
        ["python", "-m", "validation.validate_clickstream"]
    )

    run_step(
        "Validation Purchase",
        ["python", "-m", "validation.validate_purchase"]
    )

    run_step(
        "Validation Products",
        ["python", "-m", "validation.validate_products"]
    )

    run_step(
        "Prepare Data",
        ["python", "-m", "preprocessing.prepare_data"]
    )

    run_step(
        "Feature Engineering",
        ["python", "-m", "transformation.feature_engineering"]
    )

    run_step(
        "Register Feature Store",
        ["python", "-m", "feature_store.register_features"]
    )

    run_step(
        "Prepare Training Data",
        ["python", "-m", "models.prepare_training_data"]
    )

    run_step(
        "Train Model",
        ["python", "-m", "models.train_model"]
    )

    run_step(
        "Evaluate Model",
        ["python", "-m", "models.evaluate"]
    )


if __name__ == "__main__":
    recomart_pipeline()