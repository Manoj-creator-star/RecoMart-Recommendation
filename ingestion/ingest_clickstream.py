import shutil
import time
from pathlib import Path
from datetime import datetime

from config.config import SOURCE_DIR
from config.config import CLICKSTREAM_RAW
from ingestion.logger import logger


def ingest_clickstream(max_retries=3, delay=2):
    source = SOURCE_DIR / "clickstream.csv"
    destination = CLICKSTREAM_RAW / f"clickstream_{datetime.now():%Y%m%d_%H%M%S}.csv"

    if not source.exists():
        raise FileNotFoundError(f"Source file not found: {source}")

    for attempt in range(1, max_retries + 1):
        try:
            shutil.copy(source, destination)
            logger.info("Clickstream copied successfully")
            return destination
        except Exception as exc:
            logger.exception("Clickstream ingestion failed on attempt %s", attempt)
            if attempt == max_retries:
                raise
            time.sleep(delay)


if __name__ == "__main__":
    ingest_clickstream()