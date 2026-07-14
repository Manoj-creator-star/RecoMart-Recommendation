import shutil

from datetime import datetime

from config.config import SOURCE_DIR
from config.config import CLICKSTREAM_RAW

from ingestion.logger import logger


def ingest_clickstream():

    source = SOURCE_DIR / "clickstream.csv"

    destination = CLICKSTREAM_RAW / f"clickstream_{datetime.now():%Y%m%d_%H%M%S}.csv"

    shutil.copy(source, destination)

    logger.info("Clickstream copied successfully")


if __name__ == "__main__":
    ingest_clickstream()