####### jWAR Version 5 creates jWAR leaderboard for year of interest #######
####### INCLUDES UTILITY POSITION UPDATES from v4 ######
#### Allows Users to Change/Edit player stats #####

import pandas as pd
import csv
import numpy as np
import scipy.stats as st
from matplotlib import pyplot as plt
from scipy.stats import norm
import math
import jWAR_hitting_stats
import jWAR_pitching_stats
import sys

##### STARTING INPUT #####
#season = int(input("What year are you looking for: "))
season = 2018
## Fetch hitter stats and points ##
h = jWAR_hitting_stats.jWAR_hitting_stats(season)
dfh = pd.DataFrame(h, columns=['Name','Team','Age','G','AB','PA','H','1B','2B','3B','HR','RBI','BB','IBB','HBP','SO','SB','CS','AVG','OPS','hPoints'])
dfh.drop(['Team','Age','G','AB','PA','H','1B','2B','3B','HR','RBI','BB','IBB','HBP','SO','SB','CS','AVG','OPS'],axis=1,inplace=True)
dfh.insert(loc=1,column = 'Pos_Ref',value = 'H')
#print(dfh)

##Fetch pitcher stats and points##
p = jWAR_pitching_stats.jWAR_pitching_stats(season)
dfp = pd.DataFrame(p,columns=['Name','Team','Age','G','GS','CG','IP','W','L','SV','BS','ERA','ER','H','BB','SO','HBP','pPoints'])
dfp.drop(['Team','Age','G','GS','CG','IP','W','L','SV','BS','ERA','ER','H','BB','SO','HBP'],axis=1,inplace=True)
dfp.insert(loc=1,column = 'Pos_Ref',value = 'P')
#print(dfp)

# Merge both pitching and hitting stats
df = pd.merge(dfp,dfh, on=['Name','Pos_Ref'], how = 'outer')

# bring in player list for position reference
sys.path.insert(1, 'Yearly_Stat_References/Fantrax_Player_List/')
file= open('Yearly_Stat_References/Fantrax_Player_List/Fantrax_EOY_{}.csv'.format(season))
dfcsv = pd.read_csv(file)
dffs = pd.DataFrame(dfcsv,columns=['Player','Team','Position','Rk','Status','Age','Opponent','FPts','FP/G','% Owned','+/-'])
dff = dffs.loc[lambda dff: dff['FPts'] > 50, :]
dff.drop(['Status','Opponent','Age','Rk','FPts','FP/G','% Owned','+/-'],axis=1, inplace = True)
dff.rename(columns = {'Player':'Name'},inplace=True)
#print(dff)

#Add Positional Reference for Fantrax stats
pos_ref_f = []
for pos_ in dff['Position']:
    if pos_ == 'SP':
        pos_ref_f.append('P')
    elif pos_ == 'RP':
        pos_ref_f.append('P')
    elif pos_ == 'SP,RP' :
        pos_ref_f.append('P')
    elif pos_ == 'RP,SP':
        pos_ref_f.append('P')
    else:
        pos_ref_f.append('H')
pos_ref_ff = np.array(pos_ref_f)
pos_ref_ = pos_ref_ff.reshape(len(dff),1)

dff.insert(loc=1,column = 'Pos_Ref',value = pos_ref_)
#print(dff)

dffu = pd.merge(df,dff, on=['Name','Pos_Ref'],how = 'left')
dffu['Points'] = dffu[['pPoints','hPoints']].sum(axis=1)
#print(dffu)

#Create seperate columns for each position
try:
    dffu[['Pos1','Pos2','Pos3','Pos4']] = dffu['Position'].str.split(',',expand=True)
except Exception:
    try:
        dffu[['Pos1','Pos2','Pos3']] = dffu['Position'].str.split(',',expand=True)
    except Exception:
        dffu[['Pos1','Pos2']] = dffu['Position'].str.split(',',expand=True)
dffu.drop(['pPoints','hPoints','Position'],axis=1,inplace=True)
dffs = dffu.sort_values('Points',ascending=False)
dfff = dffs.dropna(subset = ["Pos1"])
#print(dfff)
#print(dfff[dfff['Name']== 'Jose Martinez'])


#Add columns to show jWAR per position
x = len(dfff)
posjWAR = np.zeros(x)
#print(posjWAR)
posjWAR = posjWAR.reshape(x,1)
n = len(dfff.columns)
#print(posjWAR)
dfff.insert(loc = n, column = 'SP_jWAR',value = posjWAR)
dfff.insert(loc = n+1, column = 'RP_jWAR',value = posjWAR)
dfff.insert(loc = n+2, column = 'C_jWAR',value = posjWAR)
dfff.insert(loc = n+3, column = '1B_jWAR',value = posjWAR)
dfff.insert(loc = n+4, column = '2B_jWAR',value = posjWAR)
dfff.insert(loc = n+5, column = '3B_jWAR',value = posjWAR)
dfff.insert(loc = n+6, column = 'SS_jWAR',value = posjWAR)
dfff.insert(loc = n+7, column = 'OF_jWAR',value = posjWAR)
dfff.insert(loc = n+8, column = 'UT_jWAR',value = posjWAR)
#print(dfff)

##### FOR USE IN UT POSITIONAL RANKINGS ####
xu = len(dffs)
posjWAR_UT = np.zeros(xu)
nu = len(dffs.columns)
#print(posjWAR)
posjWAR_UT = posjWAR_UT.reshape(xu,1)
dffs.insert(loc = nu, column = 'SP_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+1, column = 'RP_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+2, column = 'C_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+3, column = '1B_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+4, column = '2B_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+5, column = '3B_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+6, column = 'SS_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+7, column = 'OF_jWAR',value = posjWAR_UT)
dffs.insert(loc = nu+8, column = 'UT_jWAR',value = posjWAR_UT)

#####LEAGUE SIZE, # STARTERS, POSITION#####
#print("Please input roster construction...")
SP = 5#int(input("How many SP?: "))
RP = 3#int(input("How many RP?: "))
C  = 1#int(input("How many  C?: "))
fB = 1#int(input("How many 1B?: "))
sB = 1#int(input("How many 2B?: "))
tB = 1#int(input("How many 3B?: "))
SS = 1#int(input("How many SS?: "))
OF = 3#int(input("How many OF?: "))
UT = 2#int(input("How many UT?: "))

number_teams = 14#int(input("How many teams in league?: "))
number_weeks = 24#int(input("How many weeks is your season?: "))

##LIST RANGE
#Starting Roster from user inputs
starting_roster_inputs = [SP, RP, C, fB, sB, tB, SS, OF, UT]
starting_roster = ['SP', 'RP', 'C', '1B', '2B', '3B', 'SS', 'OF', 'UT']

#Create itemized roster contruction
#['SP','SP','SP','RP','RP','C',...]

def total_starting_roster():
    for pos in starting_roster_inputs:
        tsr = []
        if SP > 0:
            tsr.append('SP')
            SP_ct = 1
            while SP_ct < SP:
                tsr.append('SP')
                SP_ct +=1
        else:
            print("Are you sure no SP?")

        if RP > 0:
            tsr.append('RP')
            RP_ct = 1
            while RP_ct < RP:
                tsr.append('RP')
                RP_ct +=1
        else:
            print("Are you sure no RP?")

        if C > 0:
            tsr.append('C')
            C_ct = 1
            while C_ct < C:
                tsr.append('C')
                C_ct +=1
        else:
            print("Are you sure no C?")

        if fB > 0:
            tsr.append('1B')
            fB_ct = 1
            while fB_ct < fB:
                tsr.append('1B')
                fB_ct +=1
        else:
            print("Are you sure no 1B?")

        if sB > 0:
            tsr.append('2B')
            sB_ct = 1
            while sB_ct < sB:
                tsr.append('2B')
                sB_ct +=1
        else:
            print("Are you sure no 2B?")

        if tB > 0:
            tsr.append('3B')
            tB_ct = 1
            while tB_ct < tB:
                tsr.append('3B')
                tB_ct +=1
        else:
            print("Are you sure no 3B?")

        if SS > 0:
            tsr.append('SS')
            SS_ct = 1
            while SS_ct < SS:
                tsr.append('SS')
                SS_ct +=1
        else:
            print("Are you sure no SS?")

        if OF > 0:
            tsr.append('OF')
            OF_ct = 1
            while OF_ct < OF:
                tsr.append('OF')
                OF_ct +=1
        else:
            print("Are you sure no OF?")

        if UT > 0:
            tsr.append('UT')
            UT_ct = 1
            while UT_ct < UT:
                tsr.append('UT')
                UT_ct +=1
            return tsr
        else:
            print("Are you sure no UT?")
            return tsr

#print(total_starting_roster())

#Roster based on league size and # of starters
start_ros = np.array(starting_roster_inputs,dtype=np.int32)
starting_players = number_teams*start_ros
start_players = np.array(starting_players, dtype=np.int32)


### Fetch positional rankings ###
def positional_rankings(pos):

    if pos != 'UT':
        try:
            pos_list1 = dfff[(dfff['Pos1'] == pos)]
            pos_list2 = dfff[(dfff['Pos2'] == pos)]
            pos_list3 = dfff[(dfff['Pos3'] == pos)]
            pos_list4 = dfff[(dfff['Pos4'] == pos)]

            pos_list_u = pd.concat([pos_list1,pos_list2,pos_list3,pos_list4])
            #print(pos_list_u)
        except Exception:
            try:
                pos_list1 = dfff[(dfff['Pos1'] == pos)]
                pos_list2 = dfff[(dfff['Pos2'] == pos)]
                pos_list3 = dfff[(dfff['Pos3'] == pos)]

                pos_list_u = pd.concat([pos_list1,pos_list2,pos_list3])
            except Exception:
                pos_list1 = dfff[(dfff['Pos1'] == pos)]
                pos_list2 = dfff[(dfff['Pos2'] == pos)]

                pos_list_u = pd.concat([pos_list1,pos_list2])

        pos_list = pos_list_u.sort_values('Points',ascending=False)
        #print(pos_list)

        #Fetch positonal rankings based on league size and # of starters
        pos_index = starting_roster.index(pos)

        pos_rank = pos_list.head(start_players[pos_index])
        #print(pos_rank)
        return pos_rank
    else:
        return UT_positional_rankings()

### Solve for UT positional rank ###
def UT_positional_rankings():
        pos_list_UT = dfff[(dfff['Pos1'] == 'UT')]
        pos_list_UT.to_dict('list')

        for pos in starting_roster:
            #print(pos)
            if (pos != 'UT' and pos !='SP' and pos !='RP'):
                try:
                    pos_list1_UT = dfff[(dfff['Pos1'] == pos)]
                    pos_list2_UT = dfff[(dfff['Pos2'] == pos)]
                    pos_list3_UT = dfff[(dfff['Pos3'] == pos)]
                    pos_list4_UT = dfff[(dfff['Pos4'] == pos)]

                    pos_list_UTu = pd.concat([pos_list1_UT,pos_list2_UT,pos_list3_UT,pos_list4_UT])
                    #print("pos_list_UTu:", pos_list_UTu)
                except Exception:
                    try:
                        pos_list1_UT = dfff[(dfff['Pos1'] == pos)]
                        pos_list2_UT = dfff[(dfff['Pos2'] == pos)]
                        pos_list3_UT = dfff[(dfff['Pos3'] == pos)]

                        pos_list_UTu = pd.concat([pos_list1_UT,pos_list2_UT,pos_list3_UT])
                        #print("pos_list_UTu:", pos_list_UTu)
                    except Exception:
                        pos_list1_UT = dfff[(dfff['Pos1'] == pos)]
                        pos_list2_UT = dfff[(dfff['Pos2'] == pos)]

                        pos_list_UTu = pd.concat([pos_list1_UT,pos_list2_UT])
                        #print("pos_list_UTu:", pos_list_UTu)


                pos_list_UT = pos_list_UTu.sort_values('Points',ascending=False)
                #print("pos_list_UT:", pos_list_UT)

                #Fetch positonal rankings based on league size and # of starters
                pos_rank_UT = pos_list_UT.head(start_players[starting_roster.index(pos)])
                rank_UT = pos_rank_UT['Name'].values.tolist()

                for player_name in rank_UT:
                    play_name = dffs[(dffs['Name'] == player_name)].index.values
                    dffs.drop(index=play_name,axis=0,inplace=True)
                #print(dffs)

            else:
                pass

        pos_reff = dffs[(dffs['Pos_Ref'] == 'P')].index.values
        dffs.drop(index=pos_reff,axis=0,inplace=True)
        UT_rank_ut = dffs.sort_values('Points',ascending=False)
        UT_rank_u = dffs.dropna(subset = ["Pos1"])
        UT_rank = UT_rank_u.head(start_players[starting_roster.index('UT')])
        try:
            UT_ranks = pd.DataFrame(UT_rank,columns=['Name','Pos_Ref','Team','Points','Pos1','Pos2','Pos3','Pos4','SP_jWAR','RP_jWAR','C_jWAR','1B_jWAR','2B_jWAR','3B_jWAR','SS_jWAR','OF_jWAR','UT_jWAR'])
        except Exception:
            UT_ranks = pd.DataFrame(UT_rank,columns=['Name','Pos_Ref','Team','Points','Pos1','Pos2','Pos3','SP_jWAR','RP_jWAR','C_jWAR','1B_jWAR','2B_jWAR','3B_jWAR','SS_jWAR','OF_jWAR','UT_jWAR'])
        return UT_ranks
#print(UT_positional_rankings())

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
    FPts_wk_avg = avgs[0]/number_weeks
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
   FPts_wk_avg = avgs[0]/number_weeks
   avg_weekly_total += FPts_wk_avg * pos_mult(pos)

#Determine positional weight to total avg weekly total
pos_weight_vector = []
for pos in starting_roster:
    positional_rankings(pos)
    avgs = np.mean(positional_rankings(pos), axis = 0)
    FPts_wk_avg = avgs[0]/number_weeks
    pos_weight = pos_mult(pos)*FPts_wk_avg / avg_weekly_total
    pos_weight_vector.append(pos_weight)


#########Determine Weekly Team Standard Deviation###########
stdev_weekly_total = 62
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
    FPts_wk_stdev = stdev[0]/number_weeks
    pos_stdev = FPts_wk_stdev
    stdev_week.append(pos_stdev)
#print("Stdev week: {}".format(stdev_week))

#Creates distribution based on Team avg weekly score and standard deviation
domain = np.linspace(0,800,1000)
distr = norm.pdf(domain,avg_weekly_total,stdev_weekly_total)
plt.plot(domain, distr)
#plt.show()

def replacement_level_player(pos):
    if pos == 'UT':
        r_pos_list_u = UT_positional_rankings()
    else:
        try:
            r_pos_list1 = dfff[(dfff['Pos1'] == pos)]
            r_pos_list2 = dfff[(dfff['Pos2'] == pos)]
            r_pos_list3 = dfff[(dfff['Pos3'] == pos)]
            r_pos_list4 = dfff[(dfff['Pos4'] == pos)]
            r_pos_list_u = pd.concat([r_pos_list1,r_pos_list2,r_pos_list3,r_pos_list4])
        except Exception:
            try:
                r_pos_list1 = dfff[(dfff['Pos1'] == pos)]
                r_pos_list2 = dfff[(dfff['Pos2'] == pos)]
                r_pos_list3 = dfff[(dfff['Pos3'] == pos)]
                r_pos_list_u = pd.concat([r_pos_list1,r_pos_list2,r_pos_list3])
            except Exception:
                r_pos_list1 = dfff[(dfff['Pos1'] == pos)]
                r_pos_list2 = dfff[(dfff['Pos2'] == pos)]
                r_pos_list_u = pd.concat([r_pos_list1,r_pos_list2])

    r_pos_list = r_pos_list_u.sort_values('Points',ascending=False)


    #Fetch positonal rankings based on league size and # of starters
    r_pos_index = starting_roster.index(pos)
    r_pos_rank = r_pos_list.head(start_players[r_pos_index])


    #Pull replacement player from list
    replacement_player = r_pos_rank.tail(1)
    #print("Replacement player: ", replacement_player)


    replace_player = replacement_player.values.tolist()

    player_name = replace_player[0][0]
    #print("Replacement Name: ",player_name)
    dfff.at[dfff['Name']== player_name,'{}_jWAR'.format(pos)] = 0.01

    #Fetch players weekly average
    r_player_of_interest = dfff[(dfff['Name'] == player_name)]
    r_player_stats = np.mean(r_player_of_interest, axis = 0)
    r_player_avg = r_player_stats[0]/number_weeks
    #print(r_player_avg)

    #Fetch position weekly average
    r_play = r_player_of_interest.values.tolist()
    #print(r_play)
    pos_avg_reference = weekly_reference.get('Weekly Avg')[starting_roster.index(r_play[0][4])]

    #Calculate positonal advantage
    r_pos_adv = r_player_avg - pos_avg_reference
    #print(r_pos_adv)

    #New team score with player
    r_new_team_score = avg_weekly_total + r_pos_adv
    #print(r_new_team_score)

    #Create Z-score and find percentile
    z_score = (r_new_team_score-avg_weekly_total)/stdev_weekly_total
    z_score = round(z_score,2)
    replacement_p_value = 1 - st.norm.sf(z_score)
    #print(replacement_p_value)

    replacement_level_wins = replacement_p_value * number_weeks
    #print(replacement_level_wins)

    return replacement_level_wins


#Ask for User to input player
#player_name = input("Who's jWAR would you like to know?: ")

def jWAR(player_name):
    #Fetch players weekly average
    player_of_interest = dfff[(dfff['Name'] == player_name)]
    play = player_of_interest.values.tolist()
    player_avg = play[0][3]/number_weeks
    #print("Player Avg: ",player_avg)

    i = 0
    while i < 4:
            i = i + 1
            try:
                #Fetch position weekly average
                pos_avg_reference = weekly_reference.get('Weekly Avg')[starting_roster.index(play[0][i+3])]
                #print("Pos Avg Ref: ",pos_avg_reference)

                #Grab position
                pos = play[0][i+3]
                #print("Pos: ",pos)

                #Calculate positonal advantage
                pos_adv = player_avg - pos_avg_reference
                #print("Pos Adv: ",pos_avg_reference)

                #New team score with player
                new_team_score = avg_weekly_total + pos_adv
                #print("New Team Score: ",new_team_score)

                #Create Z-score and find percentile
                z_score = (new_team_score-avg_weekly_total)/stdev_weekly_total
                z_score = round(z_score,2)
                #print("z_score: ",z_score)
                p_value = 1 - st.norm.sf(z_score)

                #Calculate expected wins
                exp_wins = p_value * number_weeks
                #print("Exp Wins: ", exp_wins)

                #print("Exp wins ", exp_wins)
                #print("{} Total Points: {}".format(player_name,play[0][2]))
                #print("{} Weekly avg: {}".format(player_name,player_avg))
                #print("{} Average: {}".format(play[0][3],pos_avg_reference) )

                jWAR = exp_wins - replacement_level_player(pos)
                #print("{}s {} jWAR: {}".format(player_name,pos,jWAR))
                dfff.at[dfff['Name']== player_name,'{}_jWAR'.format(pos)] = jWAR

                if jWAR < 0.0:

                    if play[0][1] == 'H':

                        #Fetch position weekly average
                        pos_avg_reference = weekly_reference.get('Weekly Avg')[starting_roster.index('UT')]
                        #print("Pos Avg Ref: ",pos_avg_reference)

                        #Grab position
                        pos = 'UT'
                        #print("Pos: ",pos)

                        #Calculate positonal advantage
                        pos_adv = player_avg - pos_avg_reference
                        #print("Pos Adv: ",pos_avg_reference)

                        #New team score with player
                        new_team_score = avg_weekly_total + pos_adv
                        #print("New Team Score: ",new_team_score)

                        #Create Z-score and find percentile
                        z_score = (new_team_score-avg_weekly_total)/stdev_weekly_total
                        z_score = round(z_score,2)
                        #print("z_score: ",z_score)
                        p_value = 1 - st.norm.sf(z_score)

                        #Calculate expected wins
                        exp_wins = p_value * number_weeks
                        #print("Exp Wins: ", exp_wins)

                        #print("Exp wins ", exp_wins)
                        #print("{} Total Points: {}".format(player_name,play[0][2]))
                        #print("{} Weekly avg: {}".format(player_name,player_avg))
                        #print("{} Average: {}".format(play[0][3],pos_avg_reference) )

                        jWAR = exp_wins - replacement_level_player('UT')
                        #print("{}s {} jWAR: {}".format(player_name,pos,jWAR))
                        dfff.at[dfff['Name']== player_name,'UT_jWAR'.format(pos)] = jWAR
                    else:
                        pass
                else:
                    pass

            except Exception:
                pass
    return dfff

#jWAR('Tommy Edman')
#print(dfff[dfff['Name']=='Tommy Edman'])

### Calculates jWAR for all players ###
for player_name in dfff['Name']:
    jWAR(player_name)



### Fetch positional jWAR rankings ###
for pos in starting_roster:

        pos_jWARj = dfff.loc[lambda dfff: dfff['{}_jWAR'.format(pos)]  != 0.0 , :]
        pos_jWARjj = pos_jWARj[['Name','Team','Points','{}_jWAR'.format(pos)]]
        pos_jWAR = pos_jWARjj.sort_values('{}_jWAR'.format(pos),ascending=False)
        print(pos_jWAR)
