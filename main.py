from data.schedule_calendar import schedule_next_month
from search_schedule.search import optimize_schedule
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def solution_to_dict(solution):
    result = {}
    for i, op in enumerate(solution, 1):
        if op["type"] == "2/2":
            result[f"Оператор 2/2 #{i}"] = f"Начало {op['start']}, обед {op['lunch']}"
        elif op["type"] == "5/2":
            result[f"Оператор 5/2 #{i}"] = f"Начало {op['start']}, обед {op['lunch']}"
        else:
            result[f"Оператор 2/2 ночь #{i}"] = (
                f"Начало {op['start']}, "
                f"день {op['lunch_day']}, ночь {op['lunch_night']}"
            )
    return result


def visualisation_covers(solution, demand):
    vector_len = len(solution[0]['vector'])
    result = [0] * vector_len

    for item in solution:
        vector = item["vector"]
        for i in range(len(vector)):
            result[i] += vector[i]

    plt.figure(figsize=(12, 8))
    sns.lineplot(x=range(vector_len), y=result, label="solution")
    sns.lineplot(x=range(len(demand)), y=demand, label="demand")
    plt.show()


def main():
    demand = schedule_next_month()
    best_solution, best_score = optimize_schedule(
        n_2_2=11,
        n_5_2=3,
        n_2_2_night=8,
        needs=demand,
        day_of_month=28
    )

    solution_dict = solution_to_dict(best_solution)
    visualisation_covers(best_solution, demand)
    pd.DataFrame([solution_dict]).T.to_excel(
        'Расписание на следующий месяц.xlsx'
    )
if __name__ == "__main__":
    main()