####### jWAR NFL Version 1 creates jWAR leaderboard for year of interest #######
#### Allows Users to Change/Edit player stats #####

import pandas as pd
import csv
import numpy as np
from numpy import nan
import scipy.stats as st
from matplotlib import pyplot as plt
from scipy.stats import norm
import math
import jWAR_QB_stats
import jWAR_RB_stats
import jWAR_WR_stats
import jWAR_TE_stats
import sys

##### STARTING INPUT #####

# bring in player stats from fantrax csv
sys.path.insert(1, 'Yearly_Stat_References/')
file = open('Yearly_Stat_References/Fantrax_players_football_2021_proj.csv')
stats_csv = pd.read_csv(file)
df_stats = pd.DataFrame(stats_csv,columns=['ID','Name','Team','Position','Rk','Status','Opponent','FPts','FP/G','%D','ADP','Bye','pass_yds','pass_TD','Int','rush_yds','rush_TD','rec','rec_yds','rec_TD','tgt','FL','FRTD','RtT','2RR','GP'])
df_stats.drop(['ID','Rk','Status','Opponent','FPts','FP/G','%D','ADP','Bye','FL','FRTD','RtT','2RR','GP'],axis=1, inplace = True)



#####LEAGUE SIZE, # STARTERS, POSITION#####
#print("Please input roster construction...")
QB = 2#int(input("How many QB?: "))
RB = 2#int(input("How many RB?: "))
WR = 3#int(input("How many WR?: "))
TE = 1#int(input("How many TE?: "))
FLEX = 0#int(input("How many FLEX?: "))
SFLEX = 0#int(input("How many SFLEX?: "))

number_teams = 12#int(input("How many teams in league?: "))
number_weeks = 18#int(input("How many weeks is your season?: "))

##LIST RANGE
#Starting Roster from user inputs
starting_roster_inputs = [QB, RB, WR, TE]#, FLEX, SFLEX]
starting_roster = ['QB', 'RB', 'WR', 'TE']#, 'FLEX', 'SFLEX']

#Create itemized roster contruction
#['SP','SP','SP','RP','RP','C',...]

def total_starting_roster():
    for pos in starting_roster_inputs:
        tsr = []
        if QB > 0:
            tsr.append('QB')
            QB_ct = 1
            while QB_ct < QB:
                tsr.append('QB')
                QB_ct +=1
        else:
            print("Are you sure no QB?")

        if RB > 0:
            tsr.append('RB')
            RB_ct = 1
            while RB_ct < RB:
                tsr.append('RB')
                RB_ct +=1
        else:
            print("Are you sure no RB?")

        if WR > 0:
            tsr.append('WR')
            WR_ct = 1
            while WR_ct < WR:
                tsr.append('WR')
                WR_ct +=1
        else:
            print("Are you sure no WR?")

        if TE > 0:
            tsr.append('TE')
            TE_ct = 1
            while TE_ct < TE:
                tsr.append('TE')
                TE_ct +=1
            return tsr
        else:
            print("Are you sure no TE?")
            return tsr
        """
        if FLEX > 0:
            tsr.append('FLEX')
            FLEX_ct = 1
            while FLEX_ct < FLEX:
                tsr.append('FLEX')
                FLEX_ct +=1
        else:
            print("Are you sure no FLEX?")

        if SFLEX > 0:
            tsr.append('SFLEX')
            SFLEX_ct = 1
            while SFLEX_ct < SFLEX:
                tsr.append('SFLEX')
                SFLEX_ct +=1
            return tsr
        else:
            print("Are you sure no SFLEX?")
            return tsr
            """
#print(total_starting_roster())


#Roster based on league size and # of starters
start_ros = np.array(starting_roster_inputs,dtype=np.int32)
starting_players = number_teams*start_ros
start_players = np.array(starting_players, dtype=np.int32)

#### Calculate Fantasy Points for Players ####
### Based on points settings ###

#Points per hitting stat
pass_yds_pts = float(.04)
pass_TD_pts  = float(4)
int_pts      = float(-1)
rush_yds_pts = float(.1)
rush_TD_pts  = float(6)
rec_pts      = float(0.5)
rec_yds_pts  = float(.1)
rec_TD_pts   = float(6)
tgt_pts      = float(0)

#Create array for points per stat
fantasy_pts = [pass_yds_pts,pass_TD_pts,int_pts,rush_yds_pts,rush_TD_pts,rec_pts,rec_yds_pts,rec_TD_pts,tgt_pts]
pts_fantasy = np.array(fantasy_pts)
pts_fant = pts_fantasy.reshape(9,1)

# Convert Fangraphs stats into an array of floats
fant_stats = df_stats[['pass_yds','pass_TD','Int','rush_yds','rush_TD','rec','rec_yds','rec_TD','tgt']]
fantasy_stats = np.asfarray(fant_stats)


# Multiply points per stat array by stats array
fantasy_points = fantasy_stats.dot(pts_fant)

# Add points back to initial dataframe "Fangraphs Stats"
df_stats['FPts'] = fantasy_points

#Remove players outside of top 225
df_stats = df_stats[:225]



#Fetch positional rankings
def positional_rankings(pos):

        pos_list = df_stats[(df_stats['Position'] == pos)]

        pos_list_sorted = pos_list.sort_values('FPts',ascending=False)

        #Fetch positonal rankings based on league size and # of starters
        pos_index = starting_roster.index(pos)

        pos_rank = pos_list_sorted.head(start_players[pos_index])

        return pos_rank


#Fetch position multiple to account for # players per position
def pos_mult(pos):

        #Fetch positonal avg total points based on # of starters
        pos_index = starting_roster.index(pos)

        pos_multiple = starting_roster_inputs[pos_index]

        return pos_multiple

#Create positional average list for dictionary
pos_weekly_avg = []
for pos in starting_roster:
    positional_rankings(pos)
    avgs = np.mean(positional_rankings(pos), axis = 0)

    FPts_wk_avg = avgs[9]/number_weeks
    pos_weekly_avg.append(FPts_wk_avg)
#print(pos_weekly_avg)


#Creates Reference Dictionary for Avg Weekly Points per Position
weekly_reference = {'Position':starting_roster,'Weekly Avg':pos_weekly_avg}
#print(weekly_reference)

#Determine weekly avg team score
avg_weekly_total = 0
for pos in starting_roster:
   positional_rankings(pos)
   avgs = np.mean(positional_rankings(pos), axis = 0)
   FPts_wk_avg = avgs[9]/number_weeks
   if FPts_wk_avg != nan:
       avg_weekly_total += FPts_wk_avg * pos_mult(pos)
   else:
       break
   #print("avg_weekly_total",avg_weekly_total)
#Determine positional weight to total avg weekly total
pos_weight_vector = []
for pos in starting_roster:
    positional_rankings(pos)
    avgs = np.mean(positional_rankings(pos), axis = 0)
    FPts_wk_avg = avgs[9]/number_weeks
    pos_weight = pos_mult(pos)*FPts_wk_avg / avg_weekly_total
    pos_weight_vector.append(pos_weight)


#########Determine Weekly Team Standard Deviation###########
stdev_weekly_total = 30
weekly_var = 0

### Commented out until can determine weekly stdev of scores ###
#for pos in starting_roster:
#    positional_rankings(pos)
#    stdev = np.std(positional_rankings(pos), axis = 0)
#    FPts_wk_stdev = stdev[0]/number_weeks
#    weekly_var += (FPts_wk_stdev**2) * pos_mult(pos)
#stdev_weekly_total = math.sqrt(weekly_var)

stdev_week = []
for pos in starting_roster:
    positional_rankings(pos)
    stdev = np.std(positional_rankings(pos), axis = 0)
    FPts_wk_stdev = stdev[9]/number_weeks
    pos_stdev = FPts_wk_stdev
    stdev_week.append(pos_stdev)
#print("Stdev week: {}".format(stdev_week))

#Creates distribution based on Team avg weekly score and standard deviation
domain = np.linspace(0,800,1000)
distr = norm.pdf(domain,avg_weekly_total,stdev_weekly_total)
plt.plot(domain, distr)


def replacement_level_player(pos):

        #Fetch position list
        r_pos_list = df_stats[(df_stats['Position'] == pos)]

        #Fetch positonal rankings based on league size and # of starters
        r_pos_index = starting_roster.index(pos)
        r_pos_rank = r_pos_list.head(start_players[r_pos_index])

        #Pull replacement player from list
        replacement_player = r_pos_rank.tail(1)


        replace_player = replacement_player.values.tolist()
        player_name = replace_player[0][0]

        #Fetch players weekly average
        r_player_of_interest = df_stats[(df_stats['Name'] == player_name)]
        r_player_stats = np.mean(r_player_of_interest, axis = 0)

        r_player_avg = r_player_stats[9]/number_weeks

        #Fetch position weekly average
        r_play = r_player_of_interest.values.tolist()

        pos_avg_reference = weekly_reference.get('Weekly Avg')[starting_roster.index(r_play[0][2])]


        #Calculate positonal advantage
        r_pos_adv = r_player_avg - pos_avg_reference


        #New team score with player
        r_new_team_score = avg_weekly_total + r_pos_adv


        #Create Z-score and find percentile
        z_score = (r_new_team_score-avg_weekly_total)/stdev_weekly_total
        z_score = round(z_score,2)
        replacement_p_value = 1 - st.norm.sf(z_score)

        replacement_level_wins = replacement_p_value * number_weeks

        return replacement_level_wins

#replacement_level_player('QB')

#Ask for User to input player
#player_name = input("Who's jWAR would you like to know?: ")

def jWAR(player_name):
    #Fetch players weekly average
    player_of_interest = df_stats[(df_stats['Name'] == player_name)]
    play = player_of_interest.values.tolist()
    #print(play)
    player_avg = play[0][12]/number_weeks

    #Fetch position weekly average
    pos_avg_reference = weekly_reference.get('Weekly Avg')[starting_roster.index(play[0][2])]

    #Grab position
    pos = play[0][2]

    #Calculate positonal advantage
    pos_adv = player_avg - pos_avg_reference

    #New team score with player
    new_team_score = avg_weekly_total + pos_adv

    #Create Z-score and find percentile
    z_score = (new_team_score-avg_weekly_total)/stdev_weekly_total
    z_score = round(z_score,2)
    p_value = 1 - st.norm.sf(z_score)

    #Calculate expected wins
    exp_wins = p_value * number_weeks

    #print("Exp wins ", exp_wins)
    #print("{} Total Points: {}".format(player_name,play[0][12]))
    #print("{} Weekly avg: {}".format(player_name,player_avg))
    #print("{} Average: {}".format(play[0][2],pos_avg_reference) )

    jWAR = exp_wins - replacement_level_player(pos)
    #print('{}s jWAR is: {}'.format(player_name,jWAR))
    df_stats.at[df_stats['Name']== player_name,'{}_jWAR'.format(pos)] = jWAR
    df_stats.at[df_stats['Name']== player_name,'jWAR'.format(pos)] = jWAR

    return df_stats
#jWAR(player_name)

for player_name in df_stats['Name']:
    jWAR(player_name)
#print(dfff)

### Fetch positional jWAR rankings ###
for pos in starting_roster:

    pos_jWARn = df_stats.sort_values('{}_jWAR'.format(pos),ascending=False)
    pos_jWAR = pos_jWARn.dropna(subset = ["{}_jWAR".format(pos)])
    print("{} jWAR Rankings".format(pos))
    print(pos_jWAR[['Name','Team','FPts','{}_jWAR'.format(pos)]])

#Prints consolidated list of jWAR
jWAR_rank = df_stats.sort_values('jWAR',ascending=False)
print(jWAR_rank[['Name','Team','FPts','jWAR']])
