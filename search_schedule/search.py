import numpy as np
from employee.get_random import *
from search_schedule.utils import score_schedule

def optimize_schedule(
    n_2_2,
    n_5_2,
    n_2_2_night,
    needs,
    day_of_month,
    iterations=1_000_000
):
    best_score = np.inf
    best_solution = None


    for _ in range(iterations):
        operators = []
        total_vector = np.zeros(day_of_month * 24)

        for _ in range(int(n_2_2 / 2)):
            op = random_2_2(day_of_month)
            op2 = random_2_2(day_of_month=day_of_month, skip=2)
            operators.append(op)
            operators.append(op2)
            total_vector += op["vector"]
            total_vector += op2["vector"]

        for _ in range(n_5_2):
            op = random_5_2(day_of_month)
            operators.append(op)
            total_vector += op["vector"]

#TO DO Нужно создавать по факту только 1 случайного оператора
#потом делать его зеркало и расставлять их
#вся случайность у них по сути это выбор начала ночной смены и обеда
        for _ in range(int(n_2_2_night / 2)):
            op = random_2_2_night(day_of_month)
            op2 = random_2_2_night(day_of_month=day_of_month, skip=2)
            operators.append(op)
            operators.append(op2)
            total_vector += op["vector"]
            total_vector += op2["vector"]

        score = score_schedule(total_vector, needs)

        if score < best_score:
            best_score = score
            best_solution = operators

    return best_solution, best_score
