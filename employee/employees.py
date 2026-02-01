import numpy as np

def employeer_2_2(start, lunch, day_of_month, skip=0, first_day=False):
    if not (0 <= start <= 12):
        raise ValueError(f"start вне диапазона: {start}")
    if not (0 <= lunch < 24):
        raise ValueError(f"lunch вне диапазона: {lunch}")

    day_array = [0] * 24
    for h in range(start, start + 12):
        day_array[h] = 1
    day_array[lunch] = 0

    day_off = [0] * 24

    result = []
    for _ in range(10):
        result.append(day_array.copy())
        result.append(day_array.copy())
        result.append(day_off.copy())
        result.append(day_off.copy())

    if skip:
        result = [day_off.copy() for _ in range(skip)] + result

    if first_day:
        result = result[1:]

    result = result[:day_of_month]

    assert all(len(day) == 24 for day in result), "Есть день не из 24 часов"

    return np.array(result).flatten()


def employeer_5_2(start,
                  lunch,
                  day_of_month,
                  skip=None,
                  first_day=None):
    day_array = [0] * 24
    day_array[start:start+9] = [1] * 9
    day_array[lunch] = 0

    day_off = [0] * 24

    result = [day_array, day_array, day_array, day_array, day_array, day_off, day_off] * 10

    if skip is not None and skip > 0:
        result = [day_off] * skip + result

    if first_day is not None and first_day > 0:
        result = result[first_day:]

    result = result[:day_of_month]

    return np.array(result).flatten()