import pandas as pd
from backend.utils.logger import logger
from backend.config import settings


def load_dataset():

    logger.info(
        f"Loading dataset from {settings.DATA_PATH}"
    )

    df = pd.read_parquet(
        settings.DATA_PATH
    )

    logger.info(
        f"Loaded {len(df)} records"
    )

    return df


if __name__ == "__main__":

    df = load_dataset()

    print(df.head())