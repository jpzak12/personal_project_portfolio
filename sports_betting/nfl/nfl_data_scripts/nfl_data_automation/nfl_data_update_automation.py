import pandas as pd
from pandas import isnull
import numpy as np

def nfl_data_update_automate(current_year):

    ### schedule wlines data ###
    df_schedule_old = pd.read_csv (r'data/nfl_data/old/NFL_schedules.csv')
    df_schedule_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_schedules_currentyear.csv')

    # filter schedule for < current year
    df_schedule_old = df_schedule_old[df_schedule_old['season']<current_year]

    df_schedule_new = pd.concat([df_schedule_currentyear,df_schedule_old], axis = 0, ignore_index=True)
    df_schedule_new.drop_duplicates(subset=['game_id'], keep='first')

    df_schedule_new.to_csv('data/nfl_data/combined_data/schedule.csv', index=False)

    ### Weekly Schedule data ###
    df_weekly_schedule_old = pd.read_csv (r'data/nfl_data/old/weekly_schedule.csv')
    df_weekly_schedule_currentyear = pd.read_csv (r'data/nfl_data/current_season/weekly_schedule.csv')

    # filter schedule for < current year
    df_weekly_schedule_old = df_weekly_schedule_old[df_weekly_schedule_old['year']<current_year]

    df_weekly_schedule_new = pd.concat([df_weekly_schedule_currentyear,df_weekly_schedule_old], axis = 0, ignore_index=True)
    df_weekly_schedule_new.drop_duplicates(subset=['game_str'], keep='first')

    # merge date of game on gamestring from NFL_schedule
    df_schedule_ref = df_schedule_new[['gameday','pfr']]
    df_weekly_schedule_new = df_weekly_schedule_new.merge(df_schedule_ref, left_on='game_str', right_on='pfr').drop(columns = 'game_str')
    df_weekly_schedule_new.to_csv('data/nfl_data/combined_data/weekly_schedule.csv', index=False)

    ### weekly data ###
    df_weekly_old = pd.read_csv (r'data/nfl_data/old/NFL_weekly_1999_now.csv')
    df_weekly_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_weekly_currentyear.csv')

    # filter schedule for < current year
    df_weekly_old = df_weekly_old[df_weekly_old['season']<current_year]

    df_weekly_new = pd.concat([df_weekly_currentyear,df_weekly_old], axis = 0, ignore_index=True)
    df_weekly_new.drop_duplicates(subset=['player_id', 'season', 'week'], keep='last')

    df_weekly_new.to_csv('data/nfl_data/combined_data/weekly.csv', index=False)

    ### weekly sum data ###
    df_weeklysum_old = pd.read_csv (r'data/nfl_data/old/weekly_sum_data.csv')
    df_weeklysum_currentyear = pd.read_csv (r'data/nfl_data/current_season/weekly_sum_data_current.csv')

     # filter schedule for < current year
    df_weeklysum_old = df_weeklysum_old[df_weeklysum_old['year']<current_year]

    df_weeklysum_new = pd.concat([df_weeklysum_currentyear,df_weeklysum_old], axis=0, ignore_index=True)
    df_weeklysum_new.drop_duplicates(subset=['team_name', 'week', 'year'], keep='last')

    df_weeklysum_new.to_csv('data/nfl_data/combined_data/weekly_sum.csv', index=False)

    ### weekly agg sum data ###
    df_weeklyaggsum_old = pd.read_csv (r'data/nfl_data/old/weekly_agg_sum_data.csv')
    df_weeklyaggsum_currentyear = pd.read_csv (r'data/nfl_data/current_season/weekly_agg_sum_data_current.csv')

    # filter old data for < current year
    df_weeklyaggsum_old = df_weeklyaggsum_old[df_weeklyaggsum_old['year']<current_year]

    df_weeklyaggsum_new = pd.concat([df_weeklyaggsum_currentyear,df_weeklyaggsum_old], axis=0, ignore_index=True)
    df_weeklyaggsum_new.drop_duplicates(subset=['away_name', 'week', 'year'], keep='last')

    df_weeklyaggsum_new.to_csv('data/nfl_data/combined_data/weekly_agg_sum.csv', index=False)

    ### FiveThirtyEight ELO rating ###
    df_elo_old = pd.read_csv (r'data/nfl_data/old/NFL_elo.csv')
    df_elo_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_elo_latest.csv')

    # merge ELO ratings
    df_elo_old = df_elo_old[(df_elo_old['season']<current_year) & (df_elo_old['season']>=1999)]

    df_elo_new = pd.concat([df_elo_currentyear,df_elo_old], axis=0, ignore_index=True)
    df_elo_new.drop_duplicates(subset=['date', 'team1', 'team2'], keep='first')

    df_elo_new.to_csv('data/nfl_data/combined_data/nfl_elo.csv', index=False)

    ### ESPN QBR metric ###
    df_qbr_old = pd.read_csv (r'data/nfl_data/old/NFL_qbr.csv')
    df_qbr_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_qbr_currentyear.csv')
    df_qbr_wk14fix = pd.read_csv (r'data/nfl_data/current_season/NFL_qbr_weekly_week142022_fix.csv')

    df_qbr_old = df_qbr_old[df_qbr_old['season']<current_year]

    # merge QBR data
    df_qbr_new = pd.concat([df_qbr_currentyear,df_qbr_old], axis=0, ignore_index=True)
    df_qbr_new = pd.concat([df_qbr_new,df_qbr_wk14fix], axis=0, ignore_index=True)
    df_qbr_new.drop_duplicates(subset=['season', 'week_text', 'player_id'], keep='first')

    df_qbr_new.to_csv('data/nfl_data/combined_data/nfl_qbr_weekly.csv', index=False)

     ### ESPN QBR yearly metric ###
    df_qbr_yearly_old = pd.read_csv (r'data/nfl_data/old/NFL_qbr_yearly.csv')
    df_qbr_yearly_currentyear = pd.read_csv (r'data/nfl_data/current_season/NFL_qbr_yearly_currentyear.csv')

    df_qbr_yearly_old = df_qbr_yearly_old[df_qbr_yearly_old['season']<current_year]
   
    # merge QBR data
    df_qbr_yearly_new = pd.concat([df_qbr_yearly_currentyear,df_qbr_yearly_old], axis=0, ignore_index=True)
    df_qbr_yearly_new.drop_duplicates(subset=['season', 'player_id'], keep='first')

    df_qbr_yearly_new.to_csv('data/nfl_data/combined_data/nfl_qbr_yearly.csv', index=False)

     ### Player Weekly Data ###
    df_player_weekly_before2004 = pd.read_csv (r'data/nfl_data/old/weekly_player_sum_data_before2004.csv')
    df_player_weekly_20042021 = pd.read_csv (r'data/nfl_data/old/weekly_player_sum_data_20042021.csv')
    df_player_weekly_current = pd.read_csv (r'data/nfl_data/current_season/weekly_player_sum_data_current.csv')

    # merge Player Weekly data
    df_player_weekly_new = pd.concat([df_player_weekly_20042021,df_player_weekly_before2004], axis=0, ignore_index=True)
    df_player_weekly_new = pd.concat([df_player_weekly_current,df_player_weekly_new], axis=0, ignore_index=True)
    df_player_weekly_new.drop_duplicates(subset=['player_name', 'player_id', 'game_str'], keep='first')

    df_player_weekly_new.to_csv('data/nfl_data/combined_data/nfl_player_weekly.csv', index=False)