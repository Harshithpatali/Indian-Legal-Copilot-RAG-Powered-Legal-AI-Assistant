# download_dataset.py

import pandas as pd

df = pd.read_parquet(
    "hf://datasets/ShoaibSSM/IndianLawUnified/data/train-00000-of-00001.parquet"
)

df.to_parquet(
    "data/raw/train.parquet"
)

print(df.head())
print(df.shape)