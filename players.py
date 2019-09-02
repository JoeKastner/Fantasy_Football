#%% Load libraries
import pandas as pd
import numpy as np
import re


#%% Load players into dataframe
data = pd.read_html('https://www.fantasypros.com/nfl/rankings/consensus-cheatsheets.php?partner=google_nfl_rankings_2019_fantasy%20football%20rankings%202019&gclid=Cj0KCQjw2K3rBRDiARIsAOFSW_56iGFSVZ1RBs3QJIoorGyVs3i3tA50Om6N6cqfkZSibAm1qRiQvigaAjClEALw_wcB',attrs={'id':'rank-data'})
players = pd.DataFrame(data[0])

#%% Load injuries into dataframe
data1 = pd.read_html('https://www.pro-football-reference.com/players/injuries.htm',attrs={'id':'injuries'})
injuries = pd.DataFrame(data1[0])

#%% Load player projections
data2=pd.read_html('https://www.fantasypros.com/nfl/projections/qb.php?week=draft',attrs={'id':'data'})
stats = pd.DataFrame(data2[0])


#%% Load CSV 
notes = pd.read_csv(r'/Users/joe/Documents/Projects/Fantasy_Football_2019/players.csv')

#%% Remove unneeded columns (columns 10:, column WSID and any row that has Tier in Rank)
players = players.drop(players.iloc[:, 10:100], axis = 1) 
players = players.drop(columns=['WSID'])
players = players[~players.Rank.str.contains("Tier")]

#%% Create column for position
players=players.rename(columns={'Overall (Team)':'Summary'})
players['Position'] = players['Pos'].astype(str).str[0:2]
players = players[~players.Position.str.contains('go')] #Remove 
players['Position'].loc[players.Position.str.contains('K')] = 'K' #set Kickers to K
players['Pos_Rank'] = players['Pos'].astype(str).str[2:]


#%% Split Summary column into 4 columns
sum_split=players['Summary'].str.split(' ', n=3, expand=True)
players['Team'] = sum_split[3]
players['First_Name'] = sum_split[0]
players['Last_Name'] = sum_split[2]
players['Player_ID'] = sum_split[1]
players['Name'] = players['First_Name']+' '+players['Last_Name']
players['Rank'] = players['Rank'].astype(int)
#players = players.set_index('Rank')
#players.drop(columns=['level_0','index'],inplace=True)



#%% Set column for available
players['Available'] = 'Y'
players['FTeam'] = 'FA'

#%% Merge Injuries into players
players = players.merge(injuries,how='left',left_on='Name', right_on='Player')
players = players.merge(notes,how='left',left_on='Name',right_on='Name1')
#%% Reorder columns

cols = ['Rank','Name','FTeam','Type','Position','Pos_Rank','Notes','Team','ADP','Available','Pos_x','Avg','Class','Details','Bye','Best','Worst','Std Dev','First_Name','Last_Name','Player_ID','Tm','Pos_y',
'Player','Summary','Rank1','Name1']
players=players[cols]

#%% Create function to make player not available
def assign_player(rank,t):
    players['Available'].loc[players.Rank==rank] = 'N'
    players['FTeam'].loc[players.Rank==rank] = t
    return players[players['Rank']==rank]
#NAMES:
# 1) Dad
# 2) Pete
# 3) Vinnie
# 4) Mel
# 5) Austin
# 6) Bob
# 7) Dennis
# 8) Trav
# 9) Joe
# 10) Steve
# 11) Big Vin
# 12) Kevin

def reset_player(rank):
    players['Available'].loc[players.Rank==rank] = 'Y'
    players['FTeam'].loc[players.Rank==rank] = 'FA'
    return players[players['Rank']==rank]

        
#%% Create Functions to search players
def get_player(x): #Show players by last name
    return players[players.Last_Name.str.contains(x)] 

def all_players():
    return players[players.Available!='N']

def get_stats(x):
    return stats[stats.Player.str.contains(x)]

def RB(x='Y'): #Show vailable RBs
    return players[players.Position.str.contains('RB')&players.Available.str.contains(x)]

def QB(x='Y'): #Show vailable QBs
    return players[players.Position.str.contains('QB')&players.Available.str.contains(x)]

def WR(x='Y'): #Show vailable WRs
    return players[players.Position.str.contains('WR')&players.Available.str.contains(x)]

def TE(x='Y'): #Show vailable TEs
    return players[players.Position.str.contains('TE')&players.Available.str.contains(x)]

def DEF(x='Y'): #Show vailable DEFs
    return players[players.Position.str.contains('DS')&players.Available.str.contains(x)]

def K(x='Y'): #Show vailable Kickers
    return players[players.Position.str.contains('K')&players.Available.str.contains(x)]

#%% Create functions to search teams
def show_teams(x='all'):
    if x == 'all':
        return players[players['FTeam']!='FA'].groupby(['FTeam','Position']).Position.count()
    else:
        return players[players['FTeam']==x]

#%%
def count():
    return players[players['Available']=='N'].count()

#%%
players.to_csv('/Users/joe/Documents/Projects/Fantasy_Football_2019/players.csv')

#%%
