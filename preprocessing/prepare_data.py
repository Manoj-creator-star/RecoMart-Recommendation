import json
import logging
from pathlib import Path

import pandas as pd

# =====================================================
# Logging Configuration
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# =====================================================
# Paths
# =====================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DIR = BASE_DIR / "data" / "raw"

CLICKSTREAM_DIR = RAW_DIR / "clickstream"
PURCHASE_DIR = RAW_DIR / "purchase"
PRODUCT_DIR = RAW_DIR / "products"

PROCESSED_DIR = BASE_DIR / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = PROCESSED_DIR / "prepared_dataset.csv"


# =====================================================
# Helper Function
# =====================================================

def latest_file(folder: Path, extension: str):
    """
    Returns the latest file from a folder.
    """

    files = list(folder.glob(extension))

    if not files:
        raise FileNotFoundError(f"No {extension} files found in {folder}")

    return max(files, key=lambda x: x.stat().st_mtime)


# =====================================================
# Load Clickstream
# =====================================================

def load_clickstream():

    logger.info("Loading Clickstream Data...")

    file = latest_file(CLICKSTREAM_DIR, "*.csv")

    df = pd.read_csv(file)

    logger.info(f"Loaded {len(df)} clickstream records.")

    return df


# =====================================================
# Load Purchase History
# =====================================================

def load_purchase():

    logger.info("Loading Purchase History...")

    file = latest_file(PURCHASE_DIR, "*.csv")

    df = pd.read_csv(file)

    logger.info(f"Loaded {len(df)} purchase records.")

    return df


# =====================================================
# Load Product Metadata
# =====================================================

def load_products():

    logger.info("Loading Product Metadata...")

    file = latest_file(PRODUCT_DIR, "*.json")

    with open(file, "r", encoding="utf-8") as f:

        products = json.load(f)

    df = pd.DataFrame(products)

    # Rename ID
    df.rename(columns={"id": "product_id"}, inplace=True)

    # Flatten Rating Dictionary
    df["rating_rate"] = df["rating"].apply(
        lambda x: x.get("rate") if isinstance(x, dict) else None
    )

    df["rating_count"] = df["rating"].apply(
        lambda x: x.get("count") if isinstance(x, dict) else None
    )

    df.drop(columns=["rating"], inplace=True)

    logger.info(f"Loaded {len(df)} products.")

    return df


# =====================================================
# Clean Data
# =====================================================
def clean_data(df):

    logger.info("Cleaning Dataset...")

    # ---------------------------------------
    # Remove duplicate rows
    # ---------------------------------------
    df = df.drop_duplicates()

    # Remove duplicate columns
    df = df.loc[:, ~df.columns.duplicated()]

    # ---------------------------------------
    # Fill missing values
    # ---------------------------------------
    if "event" in df.columns:
        df["event"] = df["event"].fillna("purchase")

    if "timestamp" in df.columns and "purchase_time" in df.columns:
        df["timestamp"] = df["timestamp"].fillna(df["purchase_time"])

    if "price" in df.columns:
        df["price"] = df["price"].fillna(df["price"].median())

    # ---------------------------------------
    # Convert datetime
    # ---------------------------------------
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])

    if "purchase_time" in df.columns:
        df["purchase_time"] = pd.to_datetime(df["purchase_time"])

    # ---------------------------------------
    # Standardize text columns
    # ---------------------------------------
    if "category" in df.columns:
        df["category"] = (
            df["category"]
            .str.lower()
            .str.strip()
            .str.replace(" ", "_")
        )

    if "title" in df.columns:
        df["title"] = df["title"].str.strip()

    # ---------------------------------------
    # Create derived features
    # ---------------------------------------
    if {"price", "quantity"}.issubset(df.columns):
        df["purchase_amount"] = (
            df["price"] * df["quantity"]
        )

    if "purchase_time" in df.columns:
        df["purchase_year"] = df["purchase_time"].dt.year
        df["purchase_month"] = df["purchase_time"].dt.month_name()
        df["purchase_day"] = df["purchase_time"].dt.day_name()

    # ---------------------------------------
    # Remove unnecessary columns
    # ---------------------------------------
    columns_to_drop = [
        "image",
        "description"
    ]

    existing_columns = [
        col for col in columns_to_drop
        if col in df.columns
    ]

    if existing_columns:
        df.drop(columns=existing_columns, inplace=True)

    logger.info("Cleaning Completed.")

    return df

# =====================================================
# Merge Datasets
# =====================================================

def merge_data(clickstream, purchase, products):

    logger.info("Merging Purchase History with Product Metadata...")

    purchase_product = purchase.merge(

        products,

        on="product_id",

        how="left"

    )

    logger.info("Merging Clickstream Data...")

    final = purchase_product.merge(

        clickstream,

        on=["user_id", "product_id"],

        how="left",

        suffixes=("_purchase", "_click")

    )

    logger.info(f"Merged Dataset Shape : {final.shape}")

    return final


# =====================================================
# Save Dataset
# =====================================================

def save_dataset(df):

    df.to_csv(OUTPUT_FILE, index=False)

    logger.info(f"Dataset saved to:\n{OUTPUT_FILE}")


# =====================================================
# Main Pipeline
# =====================================================

def main():

    logger.info("=" * 60)
    logger.info("DATA PREPARATION STARTED")
    logger.info("=" * 60)

    clickstream = load_clickstream()

    purchase = load_purchase()

    products = load_products()

    merged = merge_data(

        clickstream,

        purchase,

        products

    )

    cleaned = clean_data(merged)

    save_dataset(cleaned)

    logger.info("=" * 60)
    logger.info("DATA PREPARATION COMPLETED")
    logger.info("=" * 60)

    print("\n")

    print("Prepared Dataset Successfully Created")

    print(f"Rows    : {cleaned.shape[0]}")

    print(f"Columns : {cleaned.shape[1]}")

    print(f"\nSaved To:\n{OUTPUT_FILE}")


if __name__ == "__main__":

    main()