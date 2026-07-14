from ingestion.ingest_clickstream import ingest_clickstream
from ingestion.ingest_purchase import ingest_purchase
from ingestion.ingest_products import ingest_products
from ingestion.logger import logger

def run():

    logger.info("========== Pipeline Started ==========")

    ingest_clickstream()

    ingest_purchase()

    ingest_products()

    logger.info("========== Pipeline Finished ==========")


if __name__ == "__main__":

    run()