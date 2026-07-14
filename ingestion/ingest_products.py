import json
import requests

from datetime import datetime
from tenacity import retry
from tenacity import stop_after_attempt
from tenacity import wait_fixed
from config.config import API_URL
from config.config import PRODUCT_RAW
from ingestion.logger import logger

@retry(stop=stop_after_attempt(3),
       wait=wait_fixed(5))

def fetch_products():

    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    return response.json()


def ingest_products():

    products = fetch_products()
    filename = PRODUCT_RAW / f"products_{datetime.now():%Y%m%d_%H%M%S}.json"
    with open(filename, "w") as f:
        json.dump(products, f, indent=4)
    logger.info("Product catalog downloaded")

if __name__ == "__main__":

    ingest_products()