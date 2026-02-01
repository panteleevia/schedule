import numpy as np

def score_schedule(total_vector, needs):
    diff = total_vector - needs

    under = np.clip(-diff, 0, None)
    over  = np.clip(diff, 0, None)

    return (
        5 * np.sum(under ** 2) +
        1 * np.sum(over ** 2)
    )