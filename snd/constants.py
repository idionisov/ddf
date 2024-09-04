import numpy as np

track_types = np.array([1, 11, 3, 13], dtype="int")

mc_factors: dict = {
    'EMD': 0.1388888888888889,
    'NI':  2.003205128205128
}

xy_range_full: dict = {
    'min': {'x': -70, 'y': -5},
    'max': {'x':  10, 'y': 75}
}