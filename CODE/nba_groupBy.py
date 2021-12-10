import pandas as pd
import numpy as np


### import base parquet data ###
df = pd.read_parquet('../Final Raw Data Files//final_joined_base_data.parquet')
final_player_season_df = df.copy()

### define advanced metric calcs (taken directly from nba_joined_data.py) ###

def calc_efg(dataset, fgm, fg3m, fga):
	dataset['EFG'] = (dataset[fgm] + 0.5 * dataset[fg3m]) / dataset[fga]
	return dataset

def calc_ts(dataset, pts,fga,fta):
	dataset['TS'] = dataset[pts] / (2 * (dataset[fga] + 0.44 * dataset[fta]))
	return dataset

###									  ###
###									  ###
###        GroupBy Function           ###
###									  ###
###									  ###

group_by_columns = ['off_player_id','off_player_name','def_player_id','def_player_name','team_id',  'team_name', 'off_player_pos', 'def_player_pos']
sum_columns = ['matchup_min','matchup_player_pts','matchup_team_pts', 'matchup_fgm','matchup_fga', 'matchup_fg3m','matchup_ftm', 'matchup_fta']
final_player_df = df.groupby(by=group_by_columns)[sum_columns].sum().reset_index()

final_player_df = calc_efg(final_player_df, fgm='matchup_fgm', fg3m='matchup_fg3m', fga='matchup_fga')
final_player_df['matchup_efg'] = final_player_df['EFG']

final_player_df = calc_ts(final_player_df, pts='matchup_player_pts',fga='matchup_fga',fta='matchup_fta')
final_player_df['matchup_ts'] = final_player_df['TS']


###									  ###
###									  ###
###            Cleansing              ###
###									  ###
###									  ###

del final_player_df['TS']
del final_player_df['EFG']
del final_player_df['matchup_fgm']
del final_player_df['matchup_fga']
del final_player_df['matchup_fg3m']
del final_player_df['matchup_fta']
del final_player_df['matchup_ftm']

final_player_season_df['avg_team_pts'] = final_player_season_df['pts']
del final_player_season_df['pts']
del final_player_season_df['matchup_fgm']
del final_player_season_df['matchup_fga']
del final_player_season_df['matchup_fg3m']
del final_player_season_df['matchup_fta']
del final_player_season_df['matchup_ftm']

###									  ###
###									  ###
###      Grouped Data Prep/Joins      ###
###									  ###
###									  ###

final_player_df['avg_team_pts'] = 110.35 # average of following seasonal averages: 112.1, 111.8, 111.2, 106.3

## join player stats ##

player_stats_df = pd.read_csv('../Final Raw Data Files//final_player_stats_v2.csv', low_memory=False)

# drop odd columns
player_stats_df = player_stats_df.loc[player_stats_df.SEASON_ID != 'SEASON_ID']
# reduce columns
columns = ['PLAYER_ID', 'PLAYER_NAME', 'MIN','PTS','FGM','FGA','FG3M','FTA']
float_cols = ['MIN','PTS','FGM','FGA','FG3M','FTA']
player_stats_df = player_stats_df[columns]
player_stats_df[float_cols] = player_stats_df[float_cols].astype(float)

# group-by player for aggregated season results
group_by_columns = ['PLAYER_ID', 'PLAYER_NAME']
grouped_player_stats_df = player_stats_df.groupby(by=group_by_columns)[float_cols].sum().reset_index()


grouped_player_stats_df = calc_efg(grouped_player_stats_df, fgm='FGM', fg3m='FG3M', fga='FGA')
grouped_player_stats_df['off_player_efg'] = grouped_player_stats_df['EFG']
del grouped_player_stats_df['EFG']

grouped_player_stats_df = calc_ts(grouped_player_stats_df, pts='PTS',fga='FGA',fta='FTA')
grouped_player_stats_df['off_player_ts'] = grouped_player_stats_df['TS']
del grouped_player_stats_df['TS']

# final column reduction
final_stat_cols = ['PLAYER_ID', 'PLAYER_NAME', 'MIN','PTS', 'off_player_efg', 'off_player_ts']
grouped_player_stats_df = grouped_player_stats_df[final_stat_cols]

## merge into final_player_df
final_player_df = pd.merge(final_player_df, grouped_player_stats_df, how='inner', left_on=['off_player_id'], right_on=['PLAYER_ID'])

### optional check for any data that is not joined #####
# check_df = pd.merge(final_player_df, grouped_player_stats_df, how='outer', left_on=['off_player_id'], right_on=['PLAYER_ID'], indicator=True)
# print(len(final_player_df))
# print(len(check_df))
# print(check_df.query('_merge != "both"'))
# dftest = check_df.query('_merge != "both"')
# dftest.to_csv('dftest.csv')
# breakpoint()

## Final Column Cleanse ##
final_player_df = final_player_df.rename(columns={'MIN':'off_player_min','PTS':'off_player_pts'})
del final_player_df['PLAYER_ID']
del final_player_df['PLAYER_NAME']


###									  ###
###									  ###
###              Output               ###
###									  ###
###									  ###

final_player_df.to_parquet('../Final Raw Data Files//grouped_player_data.parquet')
final_player_season_df.to_parquet('../Final Raw Data Files//grouped_player_season_data.parquet')