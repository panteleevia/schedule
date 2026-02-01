from data.schedule_calendar import schedule_next_month
from search_schedule.search import optimize_schedule
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os

def solution_to_dict(solution):
    result = {}
    for i, op in enumerate(solution, 1):
        if op["type"] == "2/2":
            result[f"Оператор 2/2 #{i}"] = f"Начало {op['start']}, обед {op['lunch']}"
        elif op["type"] == "5/2":
            result[f"Оператор 5/2 #{i}"] = f"Начало {op['start']}, обед {op['lunch']}"
        elif op["type"] == "2/2 skip=2":
            result[f"Оператор 2/2 #{i} Пропуск=2"] = f"Начало {op['start']}, обед {op['lunch']}"
        else:
            result[f"Оператор 2/2 ночь #{i}"] = (
                f"Начало {op['start']}, "
                f"день {op['lunch_day']}, ночь {op['lunch_night']}"
            )
    return result


def visualisation_covers(best_vector, demand):
    plt.figure(figsize=(12, 8))
    sns.lineplot(x=range(len(best_vector)), y=best_vector, label="solution")
    sns.lineplot(x=range(len(demand)), y=demand, label="demand")
    plt.show()


def main():
    root = tk.Tk()
    root.iconbitmap("icon.ico")
    root.title("Генератор расписания")
    root.geometry("640x320")
    root.resizable(True, True)

    root.configure(bg="#1e1e1e")

    style = ttk.Style()
    style.theme_use("default")
    style.configure("TFrame", background="#1e1e1e")

    frame = ttk.Frame(root, padding=15)
    frame.pack(fill="both", expand=True)

    # --- Поля ввода ---
    ttk.Label(frame, text="Операторов 2/2").grid(row=0, column=0, sticky="w", pady=5)
    entry_22 = ttk.Entry(frame, width=10)
    entry_22.grid(row=0, column=2, pady=5)

    ttk.Label(frame, text="Операторов 5/2").grid(row=1, column=0, sticky="w", pady=5)
    entry_52 = ttk.Entry(frame, width=10)
    entry_52.grid(row=1, column=2, pady=5)

    ttk.Label(frame, text="Операторов 2/2 день ночь").grid(row=2, column=0, sticky="w", pady=5)
    entry_22_dn = ttk.Entry(frame, width=10)
    entry_22_dn.grid(row=2, column=2, pady=5)

    ttk.Label(frame, text="Попыток").grid(row=3, column=0, sticky="w", pady=5)
    iterations = ttk.Entry(frame, width=10)
    iterations.grid(row=3, column=2, pady=5)

    ttk.Label(frame, text="Сохранить в").grid(row=4, column=0, sticky="w", pady=5)

    path_entry = ttk.Entry(frame, width=50)
    path_entry.grid(row=4, column=2, pady=5, sticky="w")


    def choose_path():
        file_path = filedialog.asksaveasfilename(
            title="Сохранить расписание",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            initialfile="Расписание на следующий месяц.xlsx"
        )
        if file_path:
            path_entry.delete(0, tk.END)
            path_entry.insert(0, file_path)

    ttk.Button(frame, text="Выбрать…", command=choose_path) \
        .grid(row=4, column=3, padx=5)


    # --- Обработчик кнопки ---
    def on_generate():
        try:
            demand, first_day = schedule_next_month()
        except:
            messagebox.showerror("Ошибка", "Нет подключения к MySQL (проблема с VPN)")
            return
        try:
            best_solution, best_score, best_vector = optimize_schedule(
                n_2_2=int(entry_22.get()),
                n_5_2=int(entry_52.get()),
                needs=demand,
                day_of_month=int(len(demand) / 24),
                iterations = int(iterations.get()),
                first_day = first_day
            )

            solution_dict = solution_to_dict(best_solution)
            visualisation_covers(best_vector, demand)

            save_path = path_entry.get()

            if not save_path:
                messagebox.showerror("Ошибка", "Выберите место сохранения файла")
                return

            pd.DataFrame([solution_dict]).T.to_excel(save_path)

        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа")
            return

        # --- Модальное окно ---
        messagebox.showinfo(
            "Готово",
            "Расписание подобрано"
        )

        # --- Закрыть приложение ---
        root.destroy()

    # --- Кнопка ---
    btn = ttk.Button(frame, text="Получить расписание", command=on_generate)
    btn.grid(row=5, column=0, columnspan=2, pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()