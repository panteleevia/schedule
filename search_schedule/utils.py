import numpy as np

def score_schedule(total_vector, needs):
    error = (total_vector - needs) ** 2
    return np.std(error)