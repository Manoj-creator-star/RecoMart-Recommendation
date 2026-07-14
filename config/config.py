from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SOURCE_DIR = BASE_DIR / "data" / "source"
RAW_DIR = BASE_DIR / "data" / "raw"

CLICKSTREAM_RAW = RAW_DIR / "clickstream"
PURCHASE_RAW = RAW_DIR / "purchase"
PRODUCT_RAW = RAW_DIR / "products"

LOG_DIR = BASE_DIR / "logs"

API_URL = "https://fakestoreapi.com/products"

for folder in [
    CLICKSTREAM_RAW,
    PURCHASE_RAW,
    PRODUCT_RAW,
    LOG_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)