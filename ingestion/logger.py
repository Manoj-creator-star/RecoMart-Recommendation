import logging
from config.config import LOG_DIR

logging.basicConfig(
    filename=LOG_DIR / "ingestion.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger("RecoMart")