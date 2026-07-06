import numpy as np


def clean_json(obj):

    if isinstance(obj, np.float32):
        return float(obj)

    if isinstance(obj, np.float64):
        return float(obj)

    if isinstance(obj, np.int32):
        return int(obj)

    if isinstance(obj, np.int64):
        return int(obj)

    return obj