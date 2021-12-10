import pandas as pd
import numpy as np
###									  ###
###									  ###
###         Global Functions          ###
###									  ###
###									  ###

### define advanced metric calcs ###

def calc_efg(dataset, fgm, fg3m, fga):
	dataset['EFG'] = (dataset[fgm] + 0.5 * dataset[fg3m]) / dataset[fga]
	return dataset

def calc_ts(dataset, pts,fga,fta):
	dataset['TS'] = dataset[pts] / (2 * (dataset[fga] + 0.44 * dataset[fta]))
	return dataset

def parse_string_min(ser: pd.Series) -> pd.Series:
	return ser.str.split(':').apply(lambda x: float(x[0]) + (float(x[1]) / 60))

###									  ###
###									  ###
###  Match-Up Data: Prep & Cleansing  ###
###									  ###
###									  ###

### import matchup data ###
df = pd.read_csv('../Final Raw Data Files//full_nba_matchup_scrape.csv', low_memory=False)
# drop odd columns
df = df.loc[df.SEASON_ID != 'SEASON_ID']
# reduce columns
columns = ['SEASON_ID', 'OFF_PLAYER_ID', 'OFF_PLAYER_NAME', 'DEF_PLAYER_ID','DEF_PLAYER_NAME', 'MATCHUP_MIN', 'PLAYER_PTS','TEAM_PTS', 'MATCHUP_FGM','MATCHUP_FGA', 'MATCHUP_FG3M','MATCHUP_FTM', 'MATCHUP_FTA', 'SFL']
float_cols = ['MATCHUP_FGM', 'MATCHUP_FG3M', 'MATCHUP_FGA', 'PLAYER_PTS', 'MATCHUP_FGA', 'MATCHUP_FTA','MATCHUP_FTM']
df[float_cols] = df[float_cols].astype(float)
df.MATCHUP_MIN = parse_string_min(df.MATCHUP_MIN)

### calculate matchup_statistics and finalize matchup_df ###

df = calc_efg(df, fgm='MATCHUP_FGM', fg3m='MATCHUP_FG3M', fga='MATCHUP_FGA')
df['MATCHUP_EFG'] = df['EFG']
del df['EFG']

df = calc_ts(df, pts='PLAYER_PTS',fga='MATCHUP_FGA',fta='MATCHUP_FTA')
df['MATCHUP_TS'] = df['TS']
del df['TS']

df['MATCHUP_PLAYER_PTS'] = df['PLAYER_PTS']
df['MATCHUP_TEAM_PTS'] = df['TEAM_PTS'].astype(int)

matchup_columns = ['SEASON_ID', 'OFF_PLAYER_ID', 'OFF_PLAYER_NAME', 'DEF_PLAYER_ID','DEF_PLAYER_NAME', 'MATCHUP_MIN', 'MATCHUP_PLAYER_PTS', 'MATCHUP_TEAM_PTS', 'MATCHUP_EFG', 'MATCHUP_TS', 'MATCHUP_FGM','MATCHUP_FGA', 'MATCHUP_FG3M','MATCHUP_FTM', 'MATCHUP_FTA']
matchup_df = df[matchup_columns]

###									  ###
###									  ###
###   Player Data: Prep & Cleansing   ###
###									  ###
###									  ###

### import player totals ###
df = pd.read_csv('../Final Raw Data Files//final_player_stats_v2.csv', low_memory=False)

#reduce coluns
columns = ['SEASON_ID', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'MIN', 'FGM', 'FGA', 'FG3M','FG3A', 'FTM', 'FTA', 'PTS']
df = df[columns]

### calculate matchup_statistics and finalize matchup_df ###
df = calc_efg(df, fgm='FGM', fg3m='FG3M', fga='FGA')
df = calc_ts(df, pts='PTS',fga='FGA',fta='FTA')

df['OFF_PLAYER_MIN'] = df['MIN']
df['OFF_PLAYER_PTS'] = df['PTS']
df['OFF_PLAYER_EFG'] = df['EFG']
df['OFF_PLAYER_TS'] = df['TS']
df['OFF_TEAM_ID'] = df['TEAM_ID']

player_columns = ['SEASON_ID', 'PLAYER_ID', 'PLAYER_NAME', 'TEAM_ID', 'OFF_PLAYER_MIN', 'OFF_PLAYER_PTS', 'OFF_PLAYER_EFG', 'OFF_PLAYER_TS']
player_df = df[player_columns]

###									  ###
###									  ###
###    Team Data: Prep & Cleansing    ###
###									  ###
###									  ###

df = pd.read_csv('../Final Raw Data Files//full_nba_team_totals_scrape.csv', low_memory=False)

team_columns = ['SEASON_ID','TEAM_ID','TEAM_NAME','PTS']
team_df = df[team_columns]

###									  ###
###									  ###
###      Data Aggreation (Joins)      ###
###									  ###
###									  ###

# joining the match_up data and player data
matchup_df[['SEASON_ID','OFF_PLAYER_ID', 'DEF_PLAYER_ID']] = matchup_df[['SEASON_ID','OFF_PLAYER_ID', 'DEF_PLAYER_ID']].astype(int)
final_df = pd.merge(matchup_df, player_df, how='inner', left_on=['SEASON_ID','OFF_PLAYER_ID'], right_on=['SEASON_ID','PLAYER_ID'])

### optional check for any data that is not joined #####
# check_df = pd.merge(matchup_df, player_df, how='outer', left_on=['SEASON_ID','OFF_PLAYER_ID'], right_on=['SEASON_ID','PLAYER_ID'], indicator=True)
# print(len(final_df))
# print(len(check_df))
# print(check_df.query('_merge != "both"'))
#########################################################

# joining the player data with the team-specific data
final_df = pd.merge(final_df, team_df, how='inner', left_on=['SEASON_ID','TEAM_ID'], right_on=['SEASON_ID','TEAM_ID'])

### optional check for any data that is not joined #####
# check_df = pd.merge(final_df, team_df, how='outer', left_on=['SEASON_ID','TEAM_ID'], right_on=['SEASON_ID','TEAM_ID'], indicator=True)
# print(len(final_df))
# print(len(check_df))
# print(check_df.query('_merge != "both"'))
#########################################################

final_df['SEASON_YEAR'] = final_df.SEASON_ID.astype(str).str[1:].astype(int)
final_df = final_df.drop('SEASON_ID', 1)

positions = pd.read_csv('../Final Raw Data Files//player_positions.csv')

# manual player name updtes for consistency



change_players = {
'Frank Mason III': 'Frank Mason',
'PJ Dozier': 'P.J. Dozier',
'Derrick Walton': 'Derrick Walton Jr.',
'Derrick Walton Jr. Jr.': 'Derrick Walton Jr.'}

for old, new in change_players.items():
    final_df.OFF_PLAYER_NAME = final_df.OFF_PLAYER_NAME.str.replace(old,new)
    final_df.DEF_PLAYER_NAME = final_df.DEF_PLAYER_NAME.str.replace(old,new)


final_df = final_df.merge(
    positions, left_on='OFF_PLAYER_NAME', right_on='Player', how='left').rename(columns={'Pos': 'off_player_pos'}).drop('Player', 1).merge(
    positions, left_on='DEF_PLAYER_NAME', right_on='Player', how='left').rename(columns={'Pos': 'def_player_pos'}).drop('Player', 1)



final_df.columns = final_df.columns.str.lower()
final_df = final_df.drop(['player_id', 'player_name'], 1)

final_df.to_parquet('../Final Raw Data Files//final_joined_base_data.parquet')
