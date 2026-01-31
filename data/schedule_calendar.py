import pandas as pd
from data.sql import get_schedule

def schedule_next_month():
    today = pd.Timestamp.today()
    first_day_next_month = (today + pd.offsets.MonthBegin(1)).normalize()
    last_day_next_month = (first_day_next_month + pd.offsets.MonthEnd(1))
    calendar = pd.date_range(
        start=first_day_next_month,
        end=last_day_next_month + pd.Timedelta(hours=23),
        freq="h"
    )
    df_calendar = pd.DataFrame({"datetime": calendar})
    df_calendar["date"] = df_calendar["datetime"].dt.date
    df_calendar["hour"] = df_calendar["datetime"].dt.hour
    df_calendar["day_number"] = df_calendar["datetime"].dt.dayofweek.apply(
        lambda x: (x + 2) if x < 6 else 1
    )
    df_calendar["day_of_week"] = df_calendar["datetime"].dt.day_name()

    df_stats = get_schedule()
    df_load_calendar = df_calendar.merge(
        df_stats,
        how="left",
        on=["day_number", "hour"]
    )

    df = df_load_calendar.copy()

    df = df.sort_values("datetime").reset_index(drop=True)

    df["t"] = df.index

    # сколько операторов нужно в каждый час
    demand = df["avg_operators_needed"].fillna(0).astype(int).tolist()

    return demand