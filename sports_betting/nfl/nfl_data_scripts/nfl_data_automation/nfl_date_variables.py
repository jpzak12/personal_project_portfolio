import pandas as pd
from pandas import isnull
import numpy as np
from datetime import datetime, timedelta

def nfl_data_date_variables():
    # find current week
    df_schedule_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_schedules_currentyear.csv')

    done = False
    d = 0
    while done == False:
            date = datetime.today() + timedelta(days=d)
            year = date.strftime("%Y")
            month = date.strftime("%m")
            day = date.strftime("%d")
            date_ref = year+"-"+month+"-"+day

            if df_schedule_currentyear["gameday"][df_schedule_currentyear["gameday"]==date_ref].count() == 0:
                d = d + 1
                print(f"Days moved forward: {d}")
                done = False
            else:
                current_week = df_schedule_currentyear["week"][df_schedule_currentyear["gameday"]==date_ref].iloc[0]
                current_season = df_schedule_currentyear["season"][df_schedule_currentyear["gameday"]==date_ref].iloc[0]
                num_games = df_schedule_currentyear["week"][df_schedule_currentyear["week"]==current_week].count()
                done = True
               
    return current_week, current_season, num_games
