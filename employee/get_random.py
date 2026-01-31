import random
from employee.employees import *

def random_2_2(day_of_month, skip=0):
    start = random.randint(7, 12)
    lunch = random.randint(start + 2, min(start + 11, 23))
    vec = employeer_2_2(start, lunch, day_of_month, skip)
    return {"type": "2/2", "start": start, "lunch": lunch, "vector": vec}

def random_5_2(day_of_month):
    start = random.randint(7, 13)
    lunch = random.randint(start + 2, min(start + 8, 23))
    vec = employeer_5_2(start, lunch, day_of_month)
    return {"type": "5/2", "start": start, "lunch": lunch, "vector": vec}

def random_2_2_night(day_of_month, skip=0):
    start = random.randint(19, 23)
    lunch_day = random.randint(10, 19)
    lunch_night = random.choice(list(range(22, 24)) + list(range(0, 6)))
    vec = employeer_2_2_night(start, lunch_day, lunch_night, day_of_month, skip)
    return {
        "type": "2/2_night",
        "start": start,
        "lunch_day": lunch_day,
        "lunch_night": lunch_night,
        "vector": vec
    }