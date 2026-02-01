import random
from employee.employees import *

def random_2_2(day_of_month, skip=0):
    start = random.randint(7, 12)
    lunch = random.randint(start + 2, start + 6)
    vec = employeer_2_2(start, lunch, day_of_month, skip)
    return {"type": "2/2", "start": start, "lunch": lunch, "vector": vec}

def random_5_2(day_of_month, first_day=0):
    start = random.randint(10, 15)
    lunch = random.randint(start + 2, start + 6)
    vec = employeer_5_2(start, lunch, day_of_month, first_day=first_day)
    return {"type": "5/2", "start": start, "lunch": lunch, "vector": vec}

def random_2_2_night(day_of_month):
    lunch_night = random.choice(list(range(0, 6)))

    vec = [2] * day_of_month * 24
    for i in range(lunch_night, len(vec), 12):
        vec[i] = 1
    return {'type': '2/2 night', 'start': 'не важно', 'lunch_night': lunch_night, 'lunch_day' : lunch_night + 12, 'vector': vec}
