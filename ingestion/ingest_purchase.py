import shutil

from datetime import datetime

from config.config import SOURCE_DIR
from config.config import PURCHASE_RAW

from ingestion.logger import logger


def ingest_purchase():

    source = SOURCE_DIR / "purchase_history.csv"

    destination = PURCHASE_RAW / f"purchase_{datetime.now():%Y%m%d_%H%M%S}.csv"

    shutil.copy(source, destination)

    logger.info("Purchase history copied successfully")


if __name__ == "__main__":
    ingest_purchase()