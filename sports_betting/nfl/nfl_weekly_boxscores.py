import pandas as pd
from pandas import isnull
import numpy as np
from sportsipy.nfl.boxscore import Boxscores, Boxscore, BoxscorePlayer
from datetime import datetime

def get_weekly_data(years_to_calc: str = "current", override: bool = False, current_week: int = 21, current_year: int = 2022):

    currentYear = current_year
    
    #initialize dataframes
    weekly_sum_data = pd.DataFrame()
    weekly_agg_sum_data = pd.DataFrame()
    weekly_player_sum_data = pd.DataFrame()
    weekly_schedule = pd.DataFrame()

    if years_to_calc == "current":
        
        y = currentYear
        start_week = 1
        # start_week = current_week - 3
        # if start_week < 1 :
        #     start_week = 1
        # else:
        #     start_week = start_week
            
        print("Starting ", y)
        weeks = list(range(start_week,24))
        end = 24

        weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule = run_data_gather(y, current_week, years_to_calc, weeks, end, weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule)
        print("Finished ", y)

    else:
        #for y in range(1999,currentYear): 
        for y in range(2018,currentYear): 

            print("Starting ", y)
            #initialize weekly data 
            if y > 2020:
                #initialize for 18 week schedule (2021-present)
                weeks = list(range(1,24))
                end = 24
            else:
                #initialize for 17 week schedule (1999-2020)
                weeks = list(range(1,23))
                end = 23

            current_week = end + 1

            weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule = run_data_gather(y, current_week, years_to_calc, weeks, end, weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule)
            
            #weekly_sum_data.to_csv('data/nfl_data/test/weekly_sum_data_2017to2021.csv', index=False)
            print("Finished ", y)

    if override == True and years_to_calc == "current":
        weekly_sum_data.to_csv('data/nfl_data/current_season/weekly_sum_data_current.csv', index=False)
        # weekly_agg_sum_data.to_csv('data/nfl_data/current_season/weekly_agg_sum_data_current.csv', index=False)
        # weekly_player_sum_data.to_csv('data/nfl_data/current_season/weekly_player_sum_data_current.csv', index=False)
        #weekly_schedule.to_csv('data/nfl_data/current_season/weekly_schedule.csv', index=False)
        pass
    elif override == True and years_to_calc != "current":
       # weekly_sum_data.to_csv('data/nfl_data/old/weekly_sum_data.csv', index=False)
        # weekly_agg_sum_data.to_csv('data/nfl_data/old/weekly_agg_sum_data.csv', index=False)
        # weekly_player_sum_data.to_csv('data/nfl_data/old/weekly_player_sum_data.csv', index=False)
        #weekly_schedule.to_csv('data/nfl_data/old/weekly_schedule.csv', index=False)
        pass
    else:
        return weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule
    

def run_data_gather(y, current_week, years_to_calc, weeks, end, weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule):

        #initialize schedules
        # schedule = get_schedule(y, weeks)
        # weekly_schedule = pd.concat([weekly_schedule, schedule])
        #print("finished schedule:",y)

        #run function to get weekly data
        weekly_data = game_data_up_to_week(weeks,y)
        print("finished weekly data:",y)
        
        weekly_sum_data = pd.concat([weekly_sum_data, weekly_data])

        # #run function to get aggregate weekly data
        # print("get agg weekly data")
        # agg_data = agg_weekly_data(schedule, weekly_data, current_week, end, weeks, y)
        # weekly_agg_sum_data = pd.concat([weekly_agg_sum_data,agg_data])

        # # run function to get weekly player data
        # weekly_player_data = player_weekly_data(schedule, current_week, end, weeks, y, years_to_calc)
        # weekly_player_sum_data = pd.concat([weekly_player_sum_data,weekly_player_data])

        return weekly_sum_data, weekly_agg_sum_data, weekly_player_sum_data, weekly_schedule
    

# get schedule data
def get_schedule(year, weeks):
    #weeks = list(range(1,20))
    schedule_df = pd.DataFrame()
    for w in range(1,len(weeks)):
        date_string = str(w) + '-' + str(year)
        week_scores = Boxscores(w,year)
        week_games_df = pd.DataFrame()
        for g in range(0,len(week_scores.games[date_string])):
            game = pd.DataFrame(week_scores.games[date_string][g], index = [0])[['away_name', 'away_abbr','home_name', 'home_abbr','winning_name', 'winning_abbr' ]]
            game['week'] = w
            game['year'] = year
            game['game_str'] = week_scores.games[date_string][g]['boxscore']
            game = game.fillna(value='Tie')
            week_games_df = pd.concat([week_games_df,game])
      
        schedule_df = pd.concat([schedule_df, week_games_df]).reset_index().drop(columns = 'index') 
    print("finished schedule...")
    return schedule_df

# get game by game data
def game_data(game_df,game_stats):
    try:
        away_team_df = game_df[['away_name', 'away_abbr', 'away_score']].rename(columns = {'away_name': 'team_name', 'away_abbr': 'team_abbr', 'away_score': 'score'})
        home_team_df = game_df[['home_name','home_abbr', 'home_score']].rename(columns = {'home_name': 'team_name', 'home_abbr': 'team_abbr', 'home_score': 'score'})
        try:
            if game_df.loc[0,'away_score'] > game_df.loc[0,'home_score']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [1], 'game_lost' : [0]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [1]}),left_index = True, right_index = True)
            elif game_df.loc[0,'away_score'] < game_df.loc[0,'home_score']:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [1]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [1], 'game_lost' : [0]}),left_index = True, right_index = True)
            else: 
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [0]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [0], 'game_lost' : [0]}),left_index = True, right_index = True)
        except TypeError:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)        

        away_stats_df = game_stats.dataframe[['away_first_downs', 'away_fourth_down_attempts',
               'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
               'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
               'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
               'away_penalties', 'away_points', 'away_rush_attempts',
               'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
               'away_third_down_conversions', 'away_time_of_possession',
               'away_times_sacked', 'away_total_yards', 'away_turnovers',
               'away_yards_from_penalties', 'away_yards_lost_from_sacks']].reset_index().drop(columns ='index').rename(columns = {
               'away_first_downs': 'first_downs', 'away_fourth_down_attempts':'fourth_down_attempts',
               'away_fourth_down_conversions':'fourth_down_conversions' , 'away_fumbles': 'fumbles', 'away_fumbles_lost': 'fumbles_lost',
               'away_interceptions': 'interceptions', 'away_net_pass_yards':'net_pass_yards' , 'away_pass_attempts': 'pass_attempts',
               'away_pass_completions':'pass_completions' , 'away_pass_touchdowns': 'pass_touchdowns', 'away_pass_yards': 'pass_yards',
               'away_penalties': 'penalties', 'away_points': 'points', 'away_rush_attempts': 'rush_attempts',
               'away_rush_touchdowns': 'rush_touchdowns', 'away_rush_yards': 'rush_yards', 'away_third_down_attempts': 'third_down_attempts',
               'away_third_down_conversions': 'third_down_conversions', 'away_time_of_possession': 'time_of_possession',
               'away_times_sacked': 'times_sacked', 'away_total_yards': 'total_yards', 'away_turnovers': 'turnovers',
               'away_yards_from_penalties':'yards_from_penalties', 'away_yards_lost_from_sacks': 'yards_lost_from_sacks'})

        home_stats_df = game_stats.dataframe[['home_first_downs', 'home_fourth_down_attempts',
               'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
               'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
               'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
               'home_penalties', 'home_points', 'home_rush_attempts',
               'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
               'home_third_down_conversions', 'home_time_of_possession',
               'home_times_sacked', 'home_total_yards', 'home_turnovers',
               'home_yards_from_penalties', 'home_yards_lost_from_sacks']].reset_index().drop(columns = 'index').rename(columns = {
               'home_first_downs': 'first_downs', 'home_fourth_down_attempts':'fourth_down_attempts',
               'home_fourth_down_conversions':'fourth_down_conversions' , 'home_fumbles': 'fumbles', 'home_fumbles_lost': 'fumbles_lost',
               'home_interceptions': 'interceptions', 'home_net_pass_yards':'net_pass_yards' , 'home_pass_attempts': 'pass_attempts',
               'home_pass_completions':'pass_completions' , 'home_pass_touchdowns': 'pass_touchdowns', 'home_pass_yards': 'pass_yards',
               'home_penalties': 'penalties', 'home_points': 'points', 'home_rush_attempts': 'rush_attempts',
               'home_rush_touchdowns': 'rush_touchdowns', 'home_rush_yards': 'rush_yards', 'home_third_down_attempts': 'third_down_attempts',
               'home_third_down_conversions': 'third_down_conversions', 'home_time_of_possession': 'time_of_possession',
               'home_times_sacked': 'times_sacked', 'home_total_yards': 'total_yards', 'home_turnovers': 'turnovers',
               'home_yards_from_penalties':'yards_from_penalties', 'home_yards_lost_from_sacks': 'yards_lost_from_sacks'})

        away_team_df = pd.merge(away_team_df, away_stats_df,left_index = True, right_index = True)
        home_team_df = pd.merge(home_team_df, home_stats_df,left_index = True, right_index = True)
        try:
            away_team_df['time_of_possession'] = (int(away_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(away_team_df['time_of_possession'].loc[0][3:5])
            home_team_df['time_of_possession'] = (int(home_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(home_team_df['time_of_possession'].loc[0][3:5])
        except TypeError:
            away_team_df['time_of_possession'] = np.nan
            home_team_df['time_of_possession'] = np.nan
    except TypeError:
        away_team_df = pd.DataFrame()
        home_team_df = pd.DataFrame()
    return away_team_df, home_team_df

def game_data_unplayed(game_df):
    away_team_df = game_df[['away_name', 'away_abbr', 'away_score']].rename(columns = {'away_name': 'team_name', 'away_abbr': 'team_abbr', 'away_score': 'score'})
    home_team_df = game_df[['home_name','home_abbr', 'home_score']].rename(columns = {'home_name': 'team_name', 'home_abbr': 'team_abbr', 'home_score': 'score'})

    away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)
    home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won' : [np.nan], 'game_lost' : [np.nan]}),left_index = True, right_index = True)

    away_stats_df = pd.DataFrame([[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]] 
                                    ,columns = ['first_downs','fourth_down_attempts','fourth_down_conversions','fumbles','fumbles_lost','interceptions','net_pass_yards','pass_attempts','pass_completions',
                                                'pass_touchdowns','pass_yards','penalties','points','rush_attempts','rush_touchdowns','rush_yards','third_down_attempts','third_down_conversions','time_of_possession','times_sacked',
                                                'total_yards','turnovers','yards_from_penalties','yards_lost_from_sacks']) 
    home_stats_df = pd.DataFrame([[np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan]] 
                                    ,columns = ['first_downs','fourth_down_attempts','fourth_down_conversions','fumbles','fumbles_lost','interceptions','net_pass_yards','pass_attempts','pass_completions',
                                                'pass_touchdowns','pass_yards','penalties','points','rush_attempts','rush_touchdowns','rush_yards','third_down_attempts','third_down_conversions','time_of_possession','times_sacked',
                                                'total_yards','turnovers','yards_from_penalties','yards_lost_from_sacks']) 
							
    away_team_df = pd.merge(away_team_df, away_stats_df,left_index = True, right_index = True)
    home_team_df = pd.merge(home_team_df, home_stats_df,left_index = True, right_index = True)
    return away_team_df, home_team_df

#prints weekly data for each team
def game_data_up_to_week(weeks,year):

    weeks_games_df = pd.DataFrame()

    for w in range(1,len(weeks)):
        print("get game data up to week:",w)

        date_string = str(w) + '-' + str(year)
        week_scores = Boxscores(w,year)
        week_games_df = pd.DataFrame()
        for g in range(0,len(week_scores.games[date_string])):
            game_str = week_scores.games[date_string][g]['boxscore']
            try:
                game_stats = Boxscore(game_str)
                game_df = pd.DataFrame(week_scores.games[date_string][g], index = [0])
                away_team_df, home_team_df = game_data(game_df,game_stats)
            except:
                away_team_df, home_team_df = game_data_unplayed(game_df)
                
            away_team_df['week'] = w
            home_team_df['week'] = w
            away_team_df['year'] = year
            home_team_df['year'] = year
            week_games_df = pd.concat([week_games_df,away_team_df])
            week_games_df = pd.concat([week_games_df,home_team_df])
        weeks_games_df = pd.concat([weeks_games_df,week_games_df])
    print("finished game_data_up_to_week...")
    return weeks_games_df

def agg_weekly_data(schedule_df,weeks_games_df,current_week,end,weeks,year):
    weeks_games_df = weeks_games_df.drop(columns = ['year'])
    schedule_df = schedule_df[schedule_df.week < end]
    agg_games_df = pd.DataFrame()
    for w in range(len(weeks)):
        print("working on week: ",w)
        # if games not played, take most recently played games
        # create game not played reference in game won column
        # once games have not played, use previously saved variables/dfs
        games_df = schedule_df[schedule_df.week == weeks[w]]
        if w >= current_week:
            w = current_week - 1 
        # use most recent week's aggregate data
        else:
            w = w

        agg_weekly_df = weeks_games_df[weeks_games_df.week < weeks[w]].drop(columns = ['score','week','game_won', 'game_lost']).groupby(by=["team_name", "team_abbr"]).mean().reset_index()
        win_loss_df = weeks_games_df[weeks_games_df.week < weeks[w]][["team_name", "team_abbr",'game_won', 'game_lost']].groupby(by=["team_name", "team_abbr"]).sum().reset_index()
        win_loss_df['win_perc'] = win_loss_df['game_won'] / (win_loss_df['game_won'] + win_loss_df['game_lost'])
        win_loss_df = win_loss_df.drop(columns = ['game_won', 'game_lost'])
        
        try:
            agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_conversions'] / agg_weekly_df['fourth_down_attempts']  
        except ZeroDivisionError:
            agg_weekly_df['fourth_down_perc'] = 0 
        agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_perc'].fillna(0)

        try:
            agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_conversions'] / agg_weekly_df['third_down_attempts']  
        except ZeroDivisionError:
            agg_weekly_df['third_down_perc'] = 0
        agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_perc'].fillna(0)  

        agg_weekly_df = agg_weekly_df.drop(columns = ['fourth_down_attempts', 'fourth_down_conversions', 'third_down_attempts', 'third_down_conversions'])
        agg_weekly_df = pd.merge(win_loss_df,agg_weekly_df,left_on = ['team_name', 'team_abbr'], right_on = ['team_name', 'team_abbr'])

        away_df = pd.merge(games_df,agg_weekly_df,how = 'inner', left_on = ['away_name', 'away_abbr'], right_on = ['team_name', 'team_abbr']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {
                'win_perc': 'away_win_perc',
               'first_downs': 'away_first_downs', 'fumbles': 'away_fumbles', 'fumbles_lost':'away_fumbles_lost', 'interceptions':'away_interceptions',
               'net_pass_yards': 'away_net_pass_yards', 'pass_attempts':'away_pass_attempts', 'pass_completions':'away_pass_completions',
               'pass_touchdowns':'away_pass_touchdowns', 'pass_yards':'away_pass_yards', 'penalties':'away_penalties', 'points':'away_points', 'rush_attempts':'away_rush_attempts',
               'rush_touchdowns':'away_rush_touchdowns', 'rush_yards':'away_rush_yards', 'time_of_possession':'away_time_of_possession', 'times_sacked':'away_times_sacked',
               'total_yards':'away_total_yards', 'turnovers':'away_turnovers', 'yards_from_penalties':'away_yards_from_penalties',
               'yards_lost_from_sacks': 'away_yards_lost_from_sacks', 'fourth_down_perc':'away_fourth_down_perc', 'third_down_perc':'away_third_down_perc'})

        home_df = pd.merge(games_df,agg_weekly_df,how = 'inner', left_on = ['home_name', 'home_abbr'], right_on = ['team_name', 'team_abbr']).drop(columns = ['team_name', 'team_abbr']).rename(columns = {
                'win_perc': 'home_win_perc',
               'first_downs': 'home_first_downs', 'fumbles': 'home_fumbles', 'fumbles_lost':'home_fumbles_lost', 'interceptions':'home_interceptions',
               'net_pass_yards': 'home_net_pass_yards', 'pass_attempts':'home_pass_attempts', 'pass_completions':'home_pass_completions',
               'pass_touchdowns':'home_pass_touchdowns', 'pass_yards':'home_pass_yards', 'penalties':'home_penalties', 'points':'home_points', 'rush_attempts':'home_rush_attempts',
               'rush_touchdowns':'home_rush_touchdowns', 'rush_yards':'home_rush_yards', 'time_of_possession':'home_time_of_possession', 'times_sacked':'home_times_sacked',
               'total_yards':'home_total_yards', 'turnovers':'home_turnovers', 'yards_from_penalties':'home_yards_from_penalties',
               'yards_lost_from_sacks': 'home_yards_lost_from_sacks', 'fourth_down_perc':'home_fourth_down_perc', 'third_down_perc':'home_third_down_perc'})

        agg_weekly_df = pd.merge(away_df,home_df,left_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
               'winning_abbr', 'week'], right_on = ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
               'winning_abbr', 'week'])

        agg_weekly_df['win_perc_dif'] = agg_weekly_df['away_win_perc'] - agg_weekly_df['home_win_perc']
        agg_weekly_df['first_downs_dif'] = agg_weekly_df['away_first_downs'] - agg_weekly_df['home_first_downs']
        agg_weekly_df['fumbles_dif'] = agg_weekly_df['away_fumbles'] - agg_weekly_df['home_fumbles']
        agg_weekly_df['interceptions_dif'] = agg_weekly_df['away_interceptions'] - agg_weekly_df['home_interceptions']
        agg_weekly_df['net_pass_yards_dif'] = agg_weekly_df['away_net_pass_yards'] - agg_weekly_df['home_net_pass_yards']
        agg_weekly_df['pass_attempts_dif'] = agg_weekly_df['away_pass_attempts'] - agg_weekly_df['home_pass_attempts']
        agg_weekly_df['pass_completions_dif'] = agg_weekly_df['away_pass_completions'] - agg_weekly_df['home_pass_completions']
        agg_weekly_df['pass_touchdowns_dif'] = agg_weekly_df['away_pass_touchdowns'] - agg_weekly_df['home_pass_touchdowns']
        agg_weekly_df['pass_yards_dif'] = agg_weekly_df['away_pass_yards'] - agg_weekly_df['home_pass_yards']
        agg_weekly_df['penalties_dif'] = agg_weekly_df['away_penalties'] - agg_weekly_df['home_penalties']
        agg_weekly_df['points_dif'] = agg_weekly_df['away_points'] - agg_weekly_df['home_points']
        agg_weekly_df['rush_attempts_dif'] = agg_weekly_df['away_rush_attempts'] - agg_weekly_df['home_rush_attempts']
        agg_weekly_df['rush_touchdowns_dif'] = agg_weekly_df['away_rush_touchdowns'] - agg_weekly_df['home_rush_touchdowns']
        agg_weekly_df['rush_yards_dif'] = agg_weekly_df['away_rush_yards'] - agg_weekly_df['home_rush_yards']
        agg_weekly_df['time_of_possession_dif'] = agg_weekly_df['away_time_of_possession'] - agg_weekly_df['home_time_of_possession']
        agg_weekly_df['times_sacked_dif'] = agg_weekly_df['away_times_sacked'] - agg_weekly_df['home_times_sacked']
        agg_weekly_df['total_yards_dif'] = agg_weekly_df['away_total_yards'] - agg_weekly_df['home_total_yards']
        agg_weekly_df['turnovers_dif'] = agg_weekly_df['away_turnovers'] - agg_weekly_df['home_turnovers']
        agg_weekly_df['yards_from_penalties_dif'] = agg_weekly_df['away_yards_from_penalties'] - agg_weekly_df['home_yards_from_penalties']
        agg_weekly_df['yards_lost_from_sacks_dif'] = agg_weekly_df['away_yards_lost_from_sacks'] - agg_weekly_df['home_yards_lost_from_sacks']
        agg_weekly_df['fourth_down_perc_dif'] = agg_weekly_df['away_fourth_down_perc'] - agg_weekly_df['home_fourth_down_perc']
        agg_weekly_df['third_down_perc_dif'] = agg_weekly_df['away_third_down_perc'] - agg_weekly_df['home_third_down_perc']

        agg_weekly_df = agg_weekly_df.drop(columns = ['away_win_perc',
               'away_first_downs', 'away_fumbles', 'away_fumbles_lost', 'away_interceptions',
               'away_net_pass_yards', 'away_pass_attempts','away_pass_completions',
               'away_pass_touchdowns', 'away_pass_yards', 'away_penalties', 'away_points', 'away_rush_attempts',
               'away_rush_touchdowns', 'away_rush_yards', 'away_time_of_possession', 'away_times_sacked',
               'away_total_yards', 'away_turnovers', 'away_yards_from_penalties',
               'away_yards_lost_from_sacks','away_fourth_down_perc', 'away_third_down_perc','home_win_perc',
               'home_first_downs', 'home_fumbles', 'home_fumbles_lost', 'home_interceptions',
               'home_net_pass_yards', 'home_pass_attempts','home_pass_completions',
               'home_pass_touchdowns', 'home_pass_yards', 'home_penalties', 'home_points', 'home_rush_attempts',
               'home_rush_touchdowns', 'home_rush_yards', 'home_time_of_possession', 'home_times_sacked',
               'home_total_yards', 'home_turnovers', 'home_yards_from_penalties',
               'home_yards_lost_from_sacks','home_fourth_down_perc', 'home_third_down_perc'])
        
        if (agg_weekly_df['winning_name'].isnull().values.any() and weeks[w] > 3):
            agg_weekly_df['result'] = np.nan
            print(f"Week {weeks[w]} games have not finished yet.")
        else:
            agg_weekly_df['result'] = agg_weekly_df['winning_name'] == agg_weekly_df['away_name']
            agg_weekly_df['result'] = agg_weekly_df['result'].astype('float')
        #agg_weekly_df = agg_weekly_df.drop(columns = ['winning_name', 'winning_abbr'])
        agg_games_df = pd.concat([agg_games_df, agg_weekly_df])
        print("finished week: ", w)
    agg_games_df = agg_games_df.reset_index().drop(columns = 'index')
    agg_games_df['year'] = year
    #agg_games_df = agg_games_df.drop(index = 20, axis=0)
    return agg_games_df

def player_weekly_data(schedule_df, current_week, end, weeks, y, years_to_calc):
    if years_to_calc == "current":
        schedule_df = schedule_df[schedule_df.week < current_week]
    else:
        schedule_df = schedule_df[schedule_df.week < end]

    print("starting weekly player data gather...")
    print(y)
    weekly_player_df = pd.DataFrame()
    for game_str in schedule_df['game_str']:

        week_games = Boxscore(game_str)

        stats = week_games.player_dict

        for key in stats.keys():
            player_data = BoxscorePlayer(key,stats[key]['name'],stats[key]['data']).dataframe
            player_data['player_id'] = key
            player_data['player_name'] = stats[key]['name']
            player_data['game_str'] = game_str
            weekly_player_df = pd.concat([weekly_player_df, player_data])
    return weekly_player_df
        