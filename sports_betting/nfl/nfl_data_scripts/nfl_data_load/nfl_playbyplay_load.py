# import packages
import pandas as pd
import plotly.graph_objects as go
import nfl_data_py as nfl
from datetime import datetime

# function to overrideif override existing csv or just pull dataframe

def get_nfl_pbp_data(type: str, override: bool = True, update: bool = True, current_season: int = 2022):
    
    #initialize current year and end year in range
    currentYear = current_season
    end_year = currentYear + 1

    # Initializing 
    # for years variables used in data pulling function
    years = []
    if update == False:
        for i in range(1999, end_year):
            years.append(i)
    else:
        years.append(currentYear)
        

        
    if type == "pbp" or type == "all":
        # load play by play data for years 1999-now
        df_pbp = nfl.import_pbp_data(years)
        if override == True and update == False:
            df_pbp.to_csv('data/nfl_data/old/NFL_pbp_1999_now.csv', index=False)
        elif override == True and update == True:
            df_pbp.to_csv('data/nfl_data/current_season/NFL_pbp_currentyear.csv', index=False)
        else:
            return df_pbp
    
    if type == "rosters" or type == "all":
        # load rosters
        df_players = nfl.import_rosters(years)
        if override == True and update == False:
            df_players.to_csv('data/nfl_data/old/NFL_rosters.csv', index=False)
        elif override == True and update == True:
            df_players.to_csv('data/nfl_data/current_season/NFL_rosters_currentyear.csv', index=False)
        else:
            return df_players

    if type == "weekly" or type == "all":
        # load weekly data
        df_weekly = nfl.import_weekly_data(years)
        if override == True and update == False:
            df_weekly.to_csv('data/nfl_data/old/NFL_weekly_1999_now.csv', index=False)
        elif override == True and update == True:
            df_weekly.to_csv('data/nfl_data/current_season/NFL_weekly_currentyear.csv', index=False)
        else:
            return df_weekly

    if type == "teams" or type == "all":
        # load team descriptions
        df_teams = nfl.import_team_desc()
        if override == True and update == False:
            df_teams.to_csv('data/nfl_data/old/NFL_teams.csv', index=False)
        elif override == True and update == True:
            df_teams.to_csv('data/nfl_data/current_season/NFL_teams_currentyear.csv', index=False)
        else:
            return df_teams

    if type == "seasonal" or type == "all":
        # load seasonal data
        df_seasonal = nfl.import_seasonal_data(years)
        if override == True and update == False:
            df_seasonal.to_csv('data/nfl_data/old/NFL_seasonal_data.csv', index=False)
        elif override == True and update == True:
            df_seasonal.to_csv('data/nfl_data/current_season/NFL_seasonal_currentyear.csv', index=False)
        else:
            return df_seasonal

    if type == "sc lines" or type == "all":
        # load scoring lines for each matchup
        df_sc_lines = nfl.import_sc_lines(years)
        if override == True and update == False:
            df_sc_lines.to_csv('data/nfl_data/old/NFL_sc_lines.csv', index=False)
        elif override == True and update == True:
            df_sc_lines.to_csv('data/nfl_data/current_season/NFL_sc_lines_currentyear.csv', index=False)
        else:
            return df_sc_lines

    if type == "win totals" or type == "all":
        # load team win totals
        df_win_totals = nfl.import_win_totals(years)
        if override == True and update == False:
            df_win_totals.to_csv('data/nfl_data/old/NFL_win_totals.csv', index=False)
        elif override == True and update == True:
            df_win_totals.to_csv('data/nfl_data/current_season/NFL_win_totals_currentyear.csv', index=False)
        else:
            return df_win_totals

    if type == "officials" or type == "all":
        # load officials
        df_officials = nfl.import_officials(years)
        if override == True and update == False:
            df_officials.to_csv('data/nfl_data/old/NFL_officials.csv', index=False)
        elif override == True and update == True:
            df_officials.to_csv('data/nfl_data/current_season/NFL_officials_currentyear.csv', index=False)
        else:
            return df_officials
    
    if type == "draft picks" or type == "all":
        # load team draft picks
        df_draft_picks = nfl.import_draft_picks(years)
        if override == True and update == False:
            df_draft_picks.to_csv('data/nfl_data/old/NFL_draft_picks.csv', index=False)
        elif override == True and update == True:
            df_draft_picks.to_csv('data/nfl_data/current_season/NFL_draft_picks_currentyear.csv', index=False)
        else:
            return df_draft_picks

    if type == "draft values" or type == "all":
        # load draft values
        df_draft_values = nfl.import_draft_values()
        if override == True and update == False:
            df_draft_values.to_csv('data/nfl_data/old/NFL_draft_values.csv', index=False)
        elif override == True and update == True:
            df_draft_values.to_csv('data/nfl_data/current_season/NFL_draft_values_currentyear.csv', index=False)
        else:
            return df_draft_values

    if type == "schedules" or type == "all":
        # load schedules
        df_schedules =  nfl.import_schedules(years)
        if override == True and update == False:
            df_schedules.to_csv('data/nfl_data/old/NFL_schedules.csv', index=False)
        elif override == True and update == True:
            df_schedules.to_csv('data/nfl_data/current_season/NFL_schedules_currentyear.csv', index=False)
        else:
            return df_schedules
    
    if type == "combine data" or type == "all":
        # load combine data
        df_combine_data = nfl.import_combine_data(years)
        if override == True and update == False:
            df_combine_data.to_csv('data/nfl_data/old/NFL_combine_data.csv', index=False)
        elif override == True and update == True:
            df_combine_data.to_csv('data/nfl_data/current_season/NFL_combine_data_currentyear.csv', index=False)
        else:
            return df_combine_data

    if type == "ids" or type == "all":
        # load ids
        df_ids =  nfl.import_ids()
        if override == True and update == False:
            df_ids.to_csv('data/nfl_data/old/NFL_ids.csv', index=False)
        elif override == True and update == True:
            df_ids.to_csv('data/nfl_data/current_season/NFL_ids_currentyear.csv', index=False)
        else:
            return df_ids

    if type == "ngs passing" or type == "all":
        # load Next Gen Stats - Passing
        df_ngs_passing = nfl.import_ngs_data( "passing" ,years)
        if override == True and update == False:
            df_ngs_passing.to_csv('data/nfl_data/old/NFL_ngs_passing.csv', index=False)
        elif override == True and update == True:
            df_ngs_passing.to_csv('data/nfl_data/current_season/NFL_ngs_passing_currentyear.csv', index=False)
        else:
            return df_ngs_passing

    if type == "ngs receiving" or type == "all":
        # load Next Gen Stats - Receiving
        df_ngs_recieving = nfl.import_ngs_data( "receiving" ,years)
        if override == True and update == False:
            df_ngs_recieving.to_csv('data/nfl_data/old/NFL_ngs_receiving.csv', index=False)
        elif override == True and update == True:
            df_ngs_recieving.to_csv('data/nfl_data/current_season/NFL_ngs_recieving_currentyear.csv', index=False)
        else:
            return df_ngs_recieving

    if type == "ngs rushing" or type == "all":
        # load Next Gen Stats - Rushing
        df_ngs_rushing = nfl.import_ngs_data( "rushing" ,years)
        if override == True and update == False:
            df_ngs_rushing.to_csv('data/nfl_data/old/NFL_ngs_rushing.csv', index=False)
        elif override == True and update == True:
            df_ngs_rushing.to_csv('data/nfl_data/current_season/NFL_ngs_rushing_currentyear.csv', index=False)
        else:
            return df_ngs_rushing

    if type == "injuries" or type == "all":
        # adjust for different year range
        years2 = [y for y in years if y > 2008]
        # load injuries
        df_injuries = nfl.import_injuries(years2)
        if override == True and update == False:
            df_injuries.to_csv('data/nfl_data/old/NFL_injuries.csv', index=False)
        elif override == True and update == True:
            df_injuries.to_csv('data/nfl_data/current_season/NFL_injuries_currentyear.csv', index=False)
        else:
            return df_injuries

    if type == "qbr" or type == "all":
        # adjust for different year range
        years3 = [y for y in years if y > 2005]
        # load QBR data
        df_qbr = nfl.import_qbr(years3, frequency="weekly")
        if override == True and update == False:
            df_qbr.to_csv('data/nfl_data/old/NFL_qbr.csv', index=False)
        elif override == True and update == True:
            df_qbr.to_csv('data/nfl_data/current_season/NFL_qbr_currentyear.csv', index=False)
        else:
            return df_qbr

    if type == "qbr_yearly" or type == "all":
        # adjust for different year range
        years3 = [y for y in years if y > 2005]
        # load QBR data
        df_qbr = nfl.import_qbr(years3)
        if override == True and update == False:
            df_qbr.to_csv('data/nfl_data/old/NFL_qbr_yearly.csv', index=False)
        elif override == True and update == True:
            df_qbr.to_csv('data/nfl_data/current_season/NFL_qbr_yearly_currentyear.csv', index=False)
        else:
            return df_qbr

    if type == "snap counts" or type == "all":
        # adjust for different year range
        years4 = [y for y in years if y > 2011]
        # load snap counts
        df_snap_counts = nfl.import_snap_counts(years4)
        if override == True and update == False:
            df_snap_counts.to_csv('data/nfl_data/old/NFL_snap_counts.csv', index=False)
        elif override == True and update == True:
            df_snap_counts.to_csv('data/nfl_data/current_season/NFL_snap_counts_currentyear.csv', index=False)
        else:
            return df_snap_counts

   




