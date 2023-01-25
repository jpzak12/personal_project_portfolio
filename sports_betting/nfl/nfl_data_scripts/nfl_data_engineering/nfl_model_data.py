import pandas as pd

# weekly data on matchup level 
# e.g. each game is one row
def model_data(override: bool = False):

    df_weekly_sum_data = pd.DataFrame()
    df_matchup_model_data = pd.DataFrame()

    weekly_model_data(override, df_weekly_sum_data)
    matchup_model_data(override, df_matchup_model_data)

    df_weekly_sum_data = pd.read_csv (r'data/nfl_data/model_data/model_prep/weekly_model_data.csv')
    df_matchup_model_data = pd.read_csv (r'data/nfl_data/model_data/model_prep/matchup_model_data.csv')
    
    rolling_avg_data = rolling_averages(df_matchup_model_data, df_weekly_sum_data)

    # past weekly data creation and loading of csv
    past_weekly_model_data(override, rolling_avg_data)
    #df_past_weekly_data = pd.read_csv (r'data/nfl_data/model_data/model_prep/past_weekly_model_data.csv')

    ## use past data to create model data set ready for training models
    # model_data = pd.merge(df_matchup_model_data,rolling_avg_data,how = 'left',left_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
    #            'winning_abbr', 'week','season'], right_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
    #            'winning_abbr', 'week','season'])

    if override == True :
       # model_data.to_csv('data/nfl_data/model_data/nfl_model_data.csv', index=False)
       pass
    else:
        return model_data

def past_weekly_model_data(override, rolling_avg_data):

    # prep weekly model data for past results
    df_weekly_model_data = rolling_avg_data


    #df_weekly_schedule = pd.read_csv(r'data/nfl_data/combined_data/weekly_schedule.csv').drop(columns = ['away_abbr', 'home_abbr', 'winning_name','winning_abbr'])
    df_weekly_schedule = pd.read_csv(r'data/nfl_data/combined_data/weekly_schedule.csv')
    df_team_ref = pd.read_csv (r'data/nfl_data/old/NFL_teams.csv')

     # add schedule string for weekly player data
    df_weekly_model_data = pd.merge(df_weekly_model_data,df_weekly_schedule,how = 'left',left_on = ['away_name', 'away_abbr','home_name', 'home_abbr','winning_name','winning_abbr','week', 'season'], right_on = ['away_name', 'away_abbr','home_name', 'home_abbr','winning_name','winning_abbr', 'week', 'year'])

   # add team name and abreviation to weekly agg data to match different abbreviations
    df_team_ref = df_team_ref[['team_name','team_abbr','team_id']]
    df_weekly_model_data = df_weekly_model_data.merge(df_team_ref, left_on='away_name', right_on='team_name').drop(columns='team_name').rename(columns = {'team_abbr':'away_abbr_ref', 'team_id':'away_team_id_ref'})
    df_weekly_model_data = df_weekly_model_data.merge(df_team_ref, left_on='home_name', right_on='team_name').drop(columns='team_name').rename(columns = {'team_abbr':'home_abbr_ref', 'team_id':'home_team_id_ref'})
    #df_weekly_model_data.to_csv('data/nfl_data/model_data/model_prep/test.csv', index=False)

    # grab elo ratings
    df_elo_weekly = elo_weekly()
    #df_elo_weekly.to_csv('data/nfl_data/model_data/model_prep/test_elo.csv', index=False)
    df_weekly_model_data = pd.merge(df_weekly_model_data,df_elo_weekly,how = 'left',left_on = ['gameday', 'away_team_id_ref', 'home_team_id_ref'], right_on = ['date', 'away_team_id_ref', 'home_team_id_ref']).drop(columns = ['date', 'away_team_name', 'home_team_name','season_y']).rename(columns={'season_x':'season'})

    #df_weekly_model_data.to_csv('data/nfl_data/model_data/model_prep/test2.csv', index=False)

    df_weekly_model_data = qbr_season(df_weekly_model_data)

    #df_weekly_model_data.to_csv('data/nfl_data/model_data/model_prep/test_qbr_yearly.csv', index=False)
    ################ left off
    df_weekly_model_data = qbr_weekly(df_weekly_model_data)

    #df_weekly_model_data.to_csv('data/nfl_data/model_data/model_prep/test_qbr_weekly.csv', index=False)
   
    if override == True :
        df_weekly_model_data.to_csv('data/nfl_data/model_data/model_prep/past_weekly_model_data.csv', index=False)
    else:
        return df_weekly_model_data

# weekly data at singular team level
# e.g. two rows for each game/team
def weekly_model_data(override, df_weekly_sum_data):

    df_team_ref = pd.read_csv (r'data/nfl_data/old/NFL_teams.csv')
    df_weekly_data = pd.read_csv (r'data/nfl_data/combined_data/weekly_sum.csv')
    df_schedules_wlines = pd.read_csv (r'data/nfl_data/combined_data/schedule.csv')

    away_lines_df = df_schedules_wlines[['season','week','away_team','total','overtime','away_rest','away_moneyline','spread_line','away_spread_odds','total_line','under_odds','over_odds','div_game','roof','surface','temp','wind','away_qb_name','away_coach','referee','stadium_id','stadium']].reset_index().drop(columns ='index').rename(columns = {
                'away_team': 'team_abbr','away_rest': 'days_rest','away_moneyline': 'moneyline','away_spread_odds': 'spread_odds','away_qb_name':'qb_name','away_coach':'coach'})
    home_lines_df = df_schedules_wlines[['season','week','home_team','total','overtime','home_rest','home_moneyline','spread_line','home_spread_odds','total_line','under_odds','over_odds','div_game','roof','surface','temp','wind','home_qb_name','home_coach','referee','stadium_id','stadium']].reset_index().drop(columns ='index').rename(columns = {
                'home_team': 'team_abbr','home_rest': 'days_rest','home_moneyline': 'moneyline','home_spread_odds': 'spread_odds','home_qb_name':'qb_name','home_coach':'coach'})
    # adjust spreadline for home_team
    home_lines_df['spread_line'] = -home_lines_df['spread_line']
    #combine away and home dfs
    lines_df = pd.concat([away_lines_df,home_lines_df])
    #lines_df = lines_df.sort_values(by=['season', 'week'])

    # merge data on team name
    df_team_ref = df_team_ref[['team_name','team_abbr','team_id']]
    df_weekly_data_merged = df_weekly_data.merge(df_team_ref, left_on='team_name', right_on='team_name').drop(columns = 'team_abbr_x').rename(columns = {'team_abbr_y': 'team_abbr','year':'season'})
    df_weekly_sum_data = df_weekly_data_merged.merge(lines_df, left_on=['season','week','team_abbr'], right_on=['season','week','team_abbr'])
    df_weekly_sum_data = df_weekly_sum_data.drop_duplicates(subset=['team_name', 'season', 'week'], keep='last')

    if override == True :
        df_weekly_sum_data.to_csv('data/nfl_data/model_data/model_prep/weekly_model_data.csv', index=False)
    else:
        return df_weekly_sum_data

# weekly data on matchup level 
# e.g. each game is one row
def matchup_model_data(override, df_matchup_model_data):

    # load team reference, weekly agg diff data, and schedule with betting lines
    df_team_ref = pd.read_csv (r'data/nfl_data/old/NFL_teams.csv')
    df_weekly_agg_data = pd.read_csv (r'data/nfl_data/combined_data/weekly_agg_sum.csv')
    df_schedules_wlines = pd.read_csv (r'data/nfl_data/combined_data/schedule.csv')

    # add team name and abreviation to weekly agg data to match different abbreviations
    df_team_ref = df_team_ref[['team_name','team_abbr','team_id']]
    df_weekly_agg_data_merged = df_weekly_agg_data.merge(df_team_ref, left_on='away_name', right_on='team_name').drop(columns='team_name').rename(columns = {'year':'season','team_abbr':'away_abbr_ref', 'team_id':'away_team_id_ref'})
    df_weekly_agg_data_merged = df_weekly_agg_data_merged.merge(df_team_ref, left_on='home_name', right_on='team_name').drop(columns='team_name').rename(columns = {'year':'season','team_abbr':'home_abbr_ref', 'team_id':'home_team_id_ref'})

    df_weekly_agg_sum_data = df_weekly_agg_data_merged.merge(df_schedules_wlines, left_on=['season','week','away_abbr_ref','home_abbr_ref'], right_on=['season','week','away_team','home_team']).drop(columns= ['away_team','home_team']).rename(columns = {'result_x':'away_win','result_y':'spread_end'})
    df_matchup_model_data = df_weekly_agg_sum_data.drop_duplicates(subset=['game_id'], keep='last')   

    ## Rearrange columns in Data ##
    game_id_col = df_matchup_model_data.pop("game_id")
    df_matchup_model_data.insert(0, "game_id", game_id_col)

    date_col = df_matchup_model_data.pop("gameday")
    df_matchup_model_data.insert(7, "gameday", date_col)

    season_col = df_matchup_model_data.pop("season")
    df_matchup_model_data.insert(8, "season", season_col)

    ### End column rearrangement ###

    if override == True :
        df_matchup_model_data.to_csv('data/nfl_data/model_data/model_prep/matchup_model_data.csv', index=False)
    else:
        return df_matchup_model_data
  

def rolling_averages(df_matchup_model_data, df_weekly_sum_data):

    try:
        df_weekly_sum_data ['fourth_down_perc'] = df_weekly_sum_data ['fourth_down_conversions'] / df_weekly_sum_data ['fourth_down_attempts']  
    except ZeroDivisionError:
        df_weekly_sum_data ['fourth_down_perc'] = 0 
    df_weekly_sum_data ['fourth_down_perc'] = df_weekly_sum_data ['fourth_down_perc'].fillna(0)

    try:
        df_weekly_sum_data ['third_down_perc'] = df_weekly_sum_data ['third_down_conversions'] / df_weekly_sum_data ['third_down_attempts']  
    except ZeroDivisionError:
        df_weekly_sum_data ['third_down_perc'] = 0
    df_weekly_sum_data ['third_down_perc'] = df_weekly_sum_data ['third_down_perc'].fillna(0)  

    df_weekly_sum_data = df_weekly_sum_data[['team_name', 'team_abbr', 'week','season',
                    'first_downs', 'fumbles', 'fumbles_lost', 'interceptions','net_pass_yards', 'pass_attempts', 'pass_completions',
                'pass_touchdowns', 'pass_yards', 'penalties', 'rush_attempts','rush_touchdowns', 'rush_yards', 'time_of_possession', 'times_sacked',
                'total_yards', 'turnovers', 'yards_from_penalties','yards_lost_from_sacks', 'fourth_down_perc', 'third_down_perc','fourth_down_attempts', 'fourth_down_conversions', 'third_down_attempts', 'third_down_conversions']]

    # sort column for rolling average
    df_weekly_sum_data.sort_values(by = ['team_name', 'season','week'], ascending = [False, False,False], na_position = 'first')

    # rolling average
    rolling_avg = 3
    df_weekly_sum_data['passing_yards_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['pass_yards'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['first_downs_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['first_downs'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['fumbles_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['fumbles'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['fumbles_lost_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['fumbles_lost'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['interceptions_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['interceptions'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['net_pass_yards_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['net_pass_yards'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['pass_attempts_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['pass_attempts'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['pass_completions_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['pass_completions'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['pass_touchdowns_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['pass_touchdowns'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['rush_attempts_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['rush_attempts'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['rush_touchdowns_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['rush_touchdowns'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['rush_yards_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['rush_yards'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['time_of_possession_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['time_of_possession'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['times_sacked_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['times_sacked'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['total_yards_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['total_yards'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['turnovers_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['turnovers'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['yards_from_penalties_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['yards_from_penalties'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['yards_lost_from_sacks_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['yards_lost_from_sacks'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['fourth_down_perc_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['fourth_down_perc'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['third_down_perc_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['third_down_perc'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    df_weekly_sum_data['penalties_3gm_rolavg'] = df_weekly_sum_data.groupby('team_abbr')['penalties'].transform(lambda x: x.rolling(rolling_avg, 1).mean())

    away_df = pd.merge(df_matchup_model_data,df_weekly_sum_data,how = 'inner', left_on = ['away_name', 'away_abbr_ref', 'week','season'], right_on = ['team_name', 'team_abbr', 'week','season']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {
                    
                'first_downs': 'away_first_downs', 'fumbles': 'away_fumbles', 'fumbles_lost':'away_fumbles_lost', 'interceptions':'away_interceptions',
                'net_pass_yards': 'away_net_pass_yards', 'pass_attempts':'away_pass_attempts', 'pass_completions':'away_pass_completions',
                'pass_touchdowns':'away_pass_touchdowns', 'pass_yards':'away_pass_yards', 'penalties':'away_penalties', 'rush_attempts':'away_rush_attempts',
                'rush_touchdowns':'away_rush_touchdowns', 'rush_yards':'away_rush_yards', 'time_of_possession':'away_time_of_possession', 'times_sacked':'away_times_sacked',
                'total_yards':'away_total_yards', 'turnovers':'away_turnovers', 'yards_from_penalties':'away_yards_from_penalties',
                'yards_lost_from_sacks': 'away_yards_lost_from_sacks', 'fourth_down_perc':'away_fourth_down_perc', 'third_down_perc':'away_third_down_perc',
                'fourth_down_attempts':'away_fourth_down_attempts', 'fourth_down_conversions':'away_fourth_down_conversions', 'third_down_attempts':'away_third_down_attempts', 'third_down_conversions':'away_third_down_conversions',
                
                'first_downs_3gm_rolavg': 'away_first_downs_3gm_rolavg', 'fumbles_3gm_rolavg': 'away_fumbles_3gm_rolavg', 'fumbles_lost_3gm_rolavg':'away_fumbles_lost_3gm_rolavg', 'interceptions_3gm_rolavg':'away_interceptions_3gm_rolavg',
                'net_pass_yards_3gm_rolavg': 'away_net_pass_yards_3gm_rolavg', 'pass_attempts_3gm_rolavg':'away_pass_attempts_3gm_rolavg', 'pass_completions_3gm_rolavg':'away_pass_completions_3gm_rolavg',
                'pass_touchdowns_3gm_rolavg':'away_pass_touchdowns_3gm_rolavg', 'passing_yards_3gm_rolavg':'away_pass_yards_3gm_rolavg', 'penalties_3gm_rolavg':'away_penalties_3gm_rolavg', 'rush_attempts_3gm_rolavg':'away_rush_attempts_3gm_rolavg',
                'rush_touchdowns_3gm_rolavg':'away_rush_touchdowns_3gm_rolavg', 'rush_yards_3gm_rolavg':'away_rush_yards_3gm_rolavg', 'time_of_possession_3gm_rolavg':'away_time_of_possession_3gm_rolavg', 'times_sacked_3gm_rolavg':'away_times_sacked_3gm_rolavg',
                'total_yards_3gm_rolavg':'away_total_yards_3gm_rolavg', 'turnovers_3gm_rolavg':'away_turnovers_3gm_rolavg', 'yards_from_penalties_3gm_rolavg':'away_yards_from_penalties_3gm_rolavg',
                'yards_lost_from_sacks_3gm_rolavg': 'away_yards_lost_from_sacks_3gm_rolavg', 'fourth_down_perc_3gm_rolavg':'away_fourth_down_perc_3gm_rolavg', 'third_down_perc_3gm_rolavg':'away_third_down_perc_3gm_rolavg',
                })

    home_df = pd.merge(df_matchup_model_data,df_weekly_sum_data,how = 'inner', left_on = ['home_name', 'home_abbr_ref', 'week','season'], right_on = ['team_name', 'team_abbr', 'week','season']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {
                
                'first_downs': 'home_first_downs', 'fumbles': 'home_fumbles', 'fumbles_lost':'home_fumbles_lost', 'interceptions':'home_interceptions',
                'net_pass_yards': 'home_net_pass_yards', 'pass_attempts':'home_pass_attempts', 'pass_completions':'home_pass_completions',
                'pass_touchdowns':'home_pass_touchdowns', 'pass_yards':'home_pass_yards', 'penalties':'home_penalties', 'rush_attempts':'home_rush_attempts',
                'rush_touchdowns':'home_rush_touchdowns', 'rush_yards':'home_rush_yards', 'time_of_possession':'home_time_of_possession', 'times_sacked':'home_times_sacked',
                'total_yards':'home_total_yards', 'turnovers':'home_turnovers', 'yards_from_penalties':'home_yards_from_penalties',
                'yards_lost_from_sacks': 'home_yards_lost_from_sacks', 'fourth_down_perc':'home_fourth_down_perc', 'third_down_perc':'home_third_down_perc',
                'fourth_down_attempts':'home_fourth_down_attempts', 'fourth_down_conversions':'home_fourth_down_conversions', 'third_down_attempts':'home_third_down_attempts', 'third_down_conversions':'home_third_down_conversions',
                
                'first_downs_3gm_rolavg': 'home_first_downs_3gm_rolavg', 'fumbles_3gm_rolavg': 'home_fumbles_3gm_rolavg', 'fumbles_lost_3gm_rolavg':'home_fumbles_lost_3gm_rolavg', 'interceptions_3gm_rolavg':'home_interceptions_3gm_rolavg',
                'net_pass_yards_3gm_rolavg': 'home_net_pass_yards_3gm_rolavg', 'pass_attempts_3gm_rolavg':'home_pass_attempts_3gm_rolavg', 'pass_completions_3gm_rolavg':'home_pass_completions_3gm_rolavg',
                'pass_touchdowns_3gm_rolavg':'home_pass_touchdowns_3gm_rolavg', 'passing_yards_3gm_rolavg':'home_pass_yards_3gm_rolavg', 'penalties_3gm_rolavg':'home_penalties_3gm_rolavg', 'rush_attempts_3gm_rolavg':'home_rush_attempts_3gm_rolavg',
                'rush_touchdowns_3gm_rolavg':'home_rush_touchdowns_3gm_rolavg', 'rush_yards_3gm_rolavg':'home_rush_yards_3gm_rolavg', 'time_of_possession_3gm_rolavg':'home_time_of_possession_3gm_rolavg', 'times_sacked_3gm_rolavg':'home_times_sacked_3gm_rolavg',
                'total_yards_3gm_rolavg':'home_total_yards_3gm_rolavg', 'turnovers_3gm_rolavg':'home_turnovers_3gm_rolavg', 'yards_from_penalties_3gm_rolavg':'home_yards_from_penalties_3gm_rolavg',
                'yards_lost_from_sacks_3gm_rolavg': 'home_yards_lost_from_sacks_3gm_rolavg', 'fourth_down_perc_3gm_rolavg':'home_fourth_down_perc_3gm_rolavg', 'third_down_perc_3gm_rolavg':'home_third_down_perc_3gm_rolavg',
                })

    away_df = away_df[['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
                'winning_abbr', 'week','season','away_first_downs', 'away_fumbles', 'away_fumbles_lost', 'away_interceptions','away_net_pass_yards', 'away_pass_attempts', 'away_pass_completions',
                'away_pass_touchdowns', 'away_pass_yards', 'away_penalties', 'away_rush_attempts','away_rush_touchdowns', 'away_rush_yards', 'away_time_of_possession', 'away_times_sacked',
                'away_total_yards', 'away_turnovers', 'away_yards_from_penalties','away_yards_lost_from_sacks', 'away_fourth_down_perc', 'away_third_down_perc','away_fourth_down_attempts', 'away_fourth_down_conversions', 'away_third_down_attempts', 
                
                 'away_first_downs_3gm_rolavg', 'away_fumbles_3gm_rolavg', 'away_fumbles_lost_3gm_rolavg', 'away_interceptions_3gm_rolavg',
                'away_net_pass_yards_3gm_rolavg', 'away_pass_attempts_3gm_rolavg', 'away_pass_completions_3gm_rolavg',
                'away_pass_touchdowns_3gm_rolavg', 'away_pass_yards_3gm_rolavg', 'away_penalties_3gm_rolavg', 'away_rush_attempts_3gm_rolavg',
                'away_rush_touchdowns_3gm_rolavg', 'away_rush_yards_3gm_rolavg', 'away_time_of_possession_3gm_rolavg', 'away_times_sacked_3gm_rolavg',
                'away_total_yards_3gm_rolavg', 'away_turnovers_3gm_rolavg', 'away_yards_from_penalties_3gm_rolavg',
                'away_yards_lost_from_sacks_3gm_rolavg', 'away_fourth_down_perc_3gm_rolavg', 'away_third_down_perc_3gm_rolavg',
                ]]

    home_df = home_df[['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
                'winning_abbr', 'week','season','home_first_downs', 'home_fumbles', 'home_fumbles_lost', 'home_interceptions','home_net_pass_yards', 'home_pass_attempts', 'home_pass_completions',
                'home_pass_touchdowns', 'home_pass_yards', 'home_penalties', 'home_rush_attempts','home_rush_touchdowns', 'home_rush_yards', 'home_time_of_possession', 'home_times_sacked',
                'home_total_yards', 'home_turnovers', 'home_yards_from_penalties','home_yards_lost_from_sacks', 'home_fourth_down_perc', 'home_third_down_perc','home_fourth_down_attempts', 'home_fourth_down_conversions', 'home_third_down_attempts', 'home_third_down_conversions',
                
                'home_first_downs_3gm_rolavg', 'home_fumbles_3gm_rolavg', 'home_fumbles_lost_3gm_rolavg', 'home_interceptions_3gm_rolavg',
                'home_net_pass_yards_3gm_rolavg', 'home_pass_attempts_3gm_rolavg', 'home_pass_completions_3gm_rolavg',
                'home_pass_touchdowns_3gm_rolavg', 'home_pass_yards_3gm_rolavg', 'home_penalties_3gm_rolavg', 'home_rush_attempts_3gm_rolavg',
                'home_rush_touchdowns_3gm_rolavg', 'home_rush_yards_3gm_rolavg', 'home_time_of_possession_3gm_rolavg', 'home_times_sacked_3gm_rolavg',
                'home_total_yards_3gm_rolavg', 'home_turnovers_3gm_rolavg', 'home_yards_from_penalties_3gm_rolavg',
                'home_yards_lost_from_sacks_3gm_rolavg', 'home_fourth_down_perc_3gm_rolavg', 'home_third_down_perc_3gm_rolavg',
                ]]

    # merge home and away stats onto matchup data
    rolling_averages = pd.merge(away_df,home_df,left_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
               'winning_abbr', 'week','season'], right_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
               'winning_abbr', 'week','season'])
    
    rolling_averages.to_csv('data/nfl_data/model_data/model_prep/test.csv', index=False)

    return rolling_averages

def elo_weekly():

    ### add ELO ratings ###
    df_elo_weekly = pd.read_csv (r'data/nfl_data/combined_data/nfl_elo.csv').drop(columns = ['score1', 'score2']).rename(columns = {
                    
                'elo1_pre': 'home_elo_pre', 'elo2_pre': 'away_elo_pre','elo_prob1': 'home_elo_prob','elo_prob2': 'away_elo_prob',
                 'qb1':'home_starting_qb','qb2':'away_starting_qb',
                'elo1_post': 'home_elo_post','elo2_post': 'away_elo_post','qbelo1_pre': 'home_qbelo_pre','qbelo2_pre': 'away_qbelo_pre',
                'qb1_value_pre': 'home_qb_value_pre','qb2_value_pre': 'away_qb_value_pre','qb1_adj': 'home_qb_adj','qb2_adj': 'away_qb_adj',
                'qbelo_prob1': 'home_qbelo_prob','qbelo_prob2': 'away_qbelo_prob','qb1_game_value': 'home_qb_game_value','qb2_game_value': 'away_qb_game_value',
                'qb1_value_post': 'home_qb_game_value_post','qb2_value_post': 'away_qb_game_value_post','qbelo1_post': 'home_qbelo_post','qbelo2_post': 'away_qbelo_post',
                'quality': 'elo_game_quality','importance': 'elo_game_importance','total_rating': 'elo_game_total_rating',"team1": "home_team_abbr","team2": "away_team_abbr"
                })
    
    # load team reference data to add team name to elo df
    df_team_ref = pd.read_csv (r'data/nfl_data/old/NFL_teams.csv')
    df_team_ref = df_team_ref[['team_name','team_abbr','team_id']]
    # merge for home and away teams
    df_elo_weekly = pd.merge(df_elo_weekly,df_team_ref, left_on='home_team_abbr', right_on='team_abbr').rename(columns = {'team_name': 'home_team_name', 'team_abbr':'home_abbr_ref', 'team_id':'home_team_id_ref'})
    df_elo_weekly = pd.merge(df_elo_weekly,df_team_ref, left_on='away_team_abbr', right_on='team_abbr').rename(columns = {'team_name': 'away_team_name', 'team_abbr':'away_abbr_ref', 'team_id':'away_team_id_ref'})

    return df_elo_weekly
    
def qbr_weekly(model_data):

    ####################################
    ### add weekly QBR ratings ###
    df_qbr_weekly = pd.read_csv (r'data/nfl_data/combined_data/nfl_qbr_weekly.csv').drop(columns = ['opp_id','opp_abb','opp_team','opp_name','week_num','qualified','name_first','name_last','week_text','team'])

    df_qbr_weekly = df_qbr_weekly[df_qbr_weekly.season_type == 'Regular']

     # load team reference data to add team name to elo df
    df_team_ref = pd.read_csv (r'data/nfl_data/old/NFL_teams.csv')
    df_team_ref = df_team_ref[['team_name','team_abbr','team_id']]
    # merge for team id
    df_qbr_weekly = pd.merge(df_qbr_weekly,df_team_ref, left_on='team_abb', right_on='team_abbr')
   
    ### Edit weekly QBR to weighted average of team per week ###
    df_qbr_total_plays = df_qbr_weekly.groupby(['season','game_week','team_id'])['qb_plays'].sum(numeric_only=True).reset_index()
    # find total team qb plays
    df_qbr_weekly = pd.merge(df_qbr_weekly,df_qbr_total_plays,how = 'left', left_on = ['season','game_week','team_id'], right_on = ['season','game_week','team_id']).rename(columns = {
    'qb_plays_x':'qb_plays_ind','qb_plays_y':'qb_plays_team'})
    # find percentage of total qb plays
    df_qbr_weekly["qb_plays_team_perc"] = df_qbr_weekly["qb_plays_ind"] / df_qbr_weekly["qb_plays_team"]
    # conditional to see if starting qb finished game or backup came in
    df_qbr_weekly['backup_qb_played'] = 0
    df_qbr_weekly.loc[df_qbr_weekly['qb_plays_team_perc'] < 1, 'backup_qb_played'] = 1
    # weighted QBR - qb_plays_team_perc * qb_plays_ind
    df_qbr_weekly["qbr_weighted_ind"] = df_qbr_weekly["qb_plays_team_perc"] * df_qbr_weekly["qbr_total"]

    # Combine weighted QBRs to get total team QBR for week
    df_qbr_weekly_team = df_qbr_weekly.groupby(['season','game_week','team_id'])['qbr_weighted_ind'].sum(numeric_only=True).reset_index().rename(columns = {'qbr_weighted_ind':'qbr_weighted_team'})

    ### Rolling avg 3 games ###
    # sort column for rolling average
    df_qbr_weekly.sort_values(by = ['season','game_week'], ascending = [False, False], na_position = 'first')

    # rolling average
    rolling_avg = 3
    df_qbr_weekly['qbr_3gm_rolavg_starter'] = df_qbr_weekly.groupby('player_id')['qbr_total'].transform(lambda x: x.rolling(rolling_avg, 1).mean())
    #df_qbr_weekly.loc[df_qbr_weekly['game_week'] == 1, 'qbr_3gm_rolavg_starter'] = 0 #find previous season QBR
    df_qbr_weekly["game_week_next"] = df_qbr_weekly["game_week"] + 1
    df_qbr_weekly = df_qbr_weekly[['name_display','game_week_next','qbr_3gm_rolavg_starter','season']]
    
    df_qbr_weekly_team = df_qbr_weekly_team[['season', 'game_week','team_id','qbr_weighted_team']]
    df_qbr_weekly_team.to_csv('data/nfl_data/test/test_qbr_weekly_team.csv', index=False)
    # merge qbr team weekly performance
    model_data = pd.merge(model_data, df_qbr_weekly_team,how = 'left', left_on = ['season','week','away_team_id_ref'], right_on = ['season','game_week','team_id']).rename(columns = {
            'qbr_weighted_team': 'away_qbr_weighted_team','backup_qb_played':'away_backup_qb_played'
            }).drop(columns=['team_id'])

    model_data.to_csv('data/nfl_data/test/test_qbr_weekly_team2.csv', index=False)

    model_data = pd.merge(model_data, df_qbr_weekly_team,how = 'left', left_on = ['home_team_id_ref','week','season'], right_on = ['team_id', 'game_week','season']).rename(columns = {
            'qbr_weighted_team': 'home_qbr_weighted_team','backup_qb_played':'home_backup_qb_played'
            }).drop(columns=['team_id'])

    # merge starter qbr rolling 3 week performance
    model_data = pd.merge(model_data, df_qbr_weekly,how = 'left', left_on = ['away_starting_qb','week','season'], right_on = ['name_display', 'game_week_next','season']).rename(columns = {
            'qbr_3gm_rolavg_starter': 'away_qbr_3gm_rolavg_starter'
            }).drop(columns=['name_display','game_week_next'])

    model_data = pd.merge(model_data, df_qbr_weekly,how = 'left', left_on = ['home_starting_qb','week','season'], right_on = ['name_display', 'game_week_next','season']).rename(columns = {
            'qbr_3gm_rolavg_starter': 'home_qbr_3gm_rolavg_starter'
            }).drop(columns=['name_display'])

    # model_data = pd.merge(model_data,df_qbr_weekly,how = 'left', left_on = ['away_abbr_ref', 'away_qb_name','week','season'], right_on = ['team_abb', 'name_display','game_week','season']).rename(columns = {
                
    #         'player_id': 'away_qbr_player_id', 'name_display': 'away_name_display', 'name_short': 'away_qb_name_short', 'rank':'away_weekly_qbr_rank', 'qbr_total':'away_qbr_weekly',
    #         'pts_added': 'away_qbr_pts_added', 'qb_plays':'away_qbr_qb_plays', 'epa_total':'away_qbr_epa_total',
    #         'pass':'away_qbr_pass', 'run':'away_qbr_run', 'exp_sack':'away_qbr_exp_sack', 'penalty':'away_qbr_penalty',
    #         'qbr_raw':'away_qbr_raw', 'sack':'away_qbr_sack', 'headshot_href':'away_qbr_headshot_href', 'game_id_x':'game_id'
            
    #         }).drop(columns=['game_week','team_abb','game_id_y','season_type'])

    # home_df = df_qbr_weekly[['team_abb', 'game_week', 'season',
    #                 'player_id', 'name_short', 'name_display','rank', 'qbr_total',
    #                 'pts_added', 'qb_plays', 'epa_total',
    #                 'pass', 'run', 'exp_sack', 'penalty',
    #                 'qbr_raw', 'sack', 'headshot_href'
    #                 ]]

    # model_data= pd.merge(model_data,home_df,how = 'left', left_on = ['home_abbr_ref', 'home_qb_name','week','season'], right_on = ['team_abb', 'name_display','game_week','season']).rename(columns = {
                
    #             'player_id': 'home_qbr_player_id', 'name_display': 'home_name_display', 'name_short': 'home_qb_name_short', 'rank':'home_weekly_qbr_rank', 'qbr_total':'home_qbr_weekly',
    #             'pts_added': 'home_qbr_pts_added', 'qb_plays':'home_qbr_qb_plays', 'epa_total':'home_qbr_epa_total',
    #             'pass':'home_qbr_pass', 'run':'home_qbr_run', 'exp_sack':'home_qbr_exp_sack', 'penalty':'home_qbr_penalty',
    #             'qbr_raw':'home_qbr_raw', 'sack':'home_qbr_sack', 'headshot_href':'home_qbr_headshot_href'
               
    #             }).drop(columns=['game_week','team_abb'])
    
    model_data = model_data.drop_duplicates(subset=[ 'season', 'week'], keep='last')

    return model_data

def qbr_season(model_data):
                                                
    ### add season QBR ratings ###
    df_qbr_yearly = pd.read_csv (r'data/nfl_data/combined_data/nfl_qbr_yearly.csv').drop(columns = ['qualified','name_first','name_last','team'])
    
    # filter for regular season QBR
    df_qbr_yearly = df_qbr_yearly[df_qbr_yearly.season_type == 'Regular']
    # create column for tying previous year QBR
    df_qbr_yearly["season_next"] = df_qbr_yearly["season"] + 1

    df_qbr_yearly = df_qbr_yearly[df_qbr_yearly.player_id != 5644]

    # if error "season not unique", eliminate duplicate players for a given year
    df_qbr_yearly = df_qbr_yearly[df_qbr_yearly.player_id != 5644]

    ## rolling 2 year QBR ##
    # sort column for rolling average
    # df_qbr_yearly.sort_values(by = ['season','player_id'], ascending = [False,False], na_position = 'first')

    # # rolling average
    # rolling_avg = 2
    # df_qbr_yearly['qbr_2yr_rolavg'] = df_qbr_yearly.groupby('player_id')['qbr_total'].transform(lambda x: x.rolling(rolling_avg, 1).mean())


    model_data = pd.merge(model_data,df_qbr_yearly,how = 'left', left_on = ['season', 'away_starting_qb'], right_on = ['season_next','name_display']).rename(columns = {
                
            'player_id': 'away_qbr_player_id_prevseason', 'name_display': 'away_name_display_prevseason','name_short': 'away_qb_name_short_prevseason', 'rank':'away_weekly_qbr_rank_prevseason', 'qbr_total':'away_qbr_weekly_prevseason',
            'pts_added': 'away_qbr_pts_added_prevseason', 'qb_plays':'away_qbr_qb_plays_prevseason', 'epa_total':'away_qbr_epa_total_prevseason',
            'pass':'away_qbr_pass_prevseason', 'run':'away_qbr_run_prevseason', 'exp_sack':'away_qbr_exp_sack_prevseason', 'penalty':'away_qbr_penalty_prevseason',
            'qbr_raw':'away_qbr_raw_prevseason', 'sack':'away_qbr_sack_prevseason', 'headshot_href':'away_qbr_headshot_href_prevseason', 'season_x':'season'
            
            }).drop(columns=['team_abb','season_type','season_next','season_y'])
    
    # model_data.to_csv('data/nfl_data/test/test_qbr_yearly_md.csv', index=False)

    home_df = df_qbr_yearly[['team_abb', 'season_next',
                    'player_id', 'name_display','name_short', 'rank', 'qbr_total',
                    'pts_added', 'qb_plays', 'epa_total',
                    'pass', 'run', 'exp_sack', 'penalty',
                    'qbr_raw', 'sack', 'headshot_href'
                    ]]
    
    # home_df.to_csv('data/nfl_data/test/test_qbr_home_df.csv', index=False)

    model_data= pd.merge(model_data,home_df,how = 'left', left_on = ['season','home_starting_qb'], right_on = ['season_next','name_display']).rename(columns = {
                
                'player_id': 'home_qbr_player_id_prevseason', 'name_display': 'home_name_display_prevseason','name_short': 'home_qb_name_short_prevseason', 'rank':'home_weekly_qbr_rank_prevseason', 'qbr_total':'home_qbr_weekly_prevseason',
                'pts_added': 'home_qbr_pts_added_prevseason', 'qb_plays':'home_qbr_qb_plays_prevseason', 'epa_total':'home_qbr_epa_total_prevseason',
                'pass':'home_qbr_pass_prevseason', 'run':'home_qbr_run_prevseason', 'exp_sack':'home_qbr_exp_sack_prevseason', 'penalty':'home_qbr_penalty_prevseason',
                'qbr_raw':'home_qbr_raw_prevseason', 'sack':'home_qbr_sack_prevseason', 'headshot_href':'home_qbr_headshot_href_prevseason'
               
                }).drop(columns=['team_abb','season_next'])

    # model_data = pd.merge(model_data,df_qbr_yearly,how = 'left', left_on = ['away_abbr_ref', 'away_qb_name','season'], right_on = ['team_abb', 'name_display','season']).rename(columns = {
                
    #         'player_id': 'away_qbr_player_id_season', 'name_display': 'away_name_display_season','name_short': 'away_qb_name_short_season', 'rank':'away_weekly_qbr_rank_season', 'qbr_total':'away_qbr_weekly_season',
    #         'pts_added': 'away_qbr_pts_added_season', 'qb_plays':'away_qbr_qb_plays_season', 'epa_total':'away_qbr_epa_total_season',
    #         'pass':'away_qbr_pass_season', 'run':'away_qbr_run_season', 'exp_sack':'away_qbr_exp_sack_season', 'penalty':'away_qbr_penalty_season',
    #         'qbr_raw':'away_qbr_raw_season', 'sack':'away_qbr_sack_season', 'headshot_href':'away_qbr_headshot_href_season'
            
    #         }).drop(columns=['team_abb','season_type'])

    # home_df = df_qbr_yearly[['team_abb', 'season',
    #                 'player_id', 'name_display','name_short', 'rank', 'qbr_total',
    #                 'pts_added', 'qb_plays', 'epa_total',
    #                 'pass', 'run', 'exp_sack', 'penalty',
    #                 'qbr_raw', 'sack', 'headshot_href'
    #                 ]]

    # model_data= pd.merge(model_data,home_df,how = 'left', left_on = ['home_abbr_ref','home_qb_name','season'], right_on = ['team_abb', 'name_display','season']).rename(columns = {
                
    #             'player_id': 'home_qbr_player_id_season', 'name_display': 'home_name_display_season','name_short': 'home_qb_name_short_season', 'rank':'home_weekly_qbr_rank_season', 'qbr_total':'home_qbr_weekly_season',
    #             'pts_added': 'home_qbr_pts_added_season', 'qb_plays':'home_qbr_qb_plays_season', 'epa_total':'home_qbr_epa_total_season',
    #             'pass':'home_qbr_pass_season', 'run':'home_qbr_run_season', 'exp_sack':'home_qbr_exp_sack_season', 'penalty':'home_qbr_penalty_season',
    #             'qbr_raw':'home_qbr_raw_season', 'sack':'home_qbr_sack_season', 'headshot_href':'home_qbr_headshot_href_season'
               
    #             }).drop(columns=['team_abb'])

    #model_data = model_data.drop_duplicates(subset=['game_id', 'season', 'week'], keep='last')

    return model_data