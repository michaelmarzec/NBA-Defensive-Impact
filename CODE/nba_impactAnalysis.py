#### NOTE: Positive is bad. Negative is good. E.g., a playerImpact_playerPtsPerMin of -1 implies that the defensive player will allow 1 less point per minute.

import pandas as pd
import numpy as np


### import base parquet datasets ###
grouped_player_data = pd.read_parquet('../Final Raw Data Files//grouped_player_data.parquet')
grouped_player_season_data = pd.read_parquet('../Final Raw Data Files//grouped_player_season_data.parquet')

## Weighted Average Function ##

def weighted_avg(df, group_by_field, field_to_average, field_for_weight):
	df.groupby(df[group_by_field]).apply(lambda x: np.average(x[field_to_average], weights=x[field_for_weight]))
	return df


###									  ###
###									  ###
###       Point Based Metrics         ###
###									  ###
###									  ###

def player_point_impact(df, matchup_min = 'matchup_min', matchup_player_pts = 'matchup_player_pts', off_player_min = 'off_player_min', off_player_pts = 'off_player_pts'):
	df['matchup_ptsPerMin'] = df[matchup_player_pts] / df[matchup_min]
	df['off_player_ptsPerMin'] = df[off_player_pts] / df[off_player_min]
	df['playerImpact_playerPtsPerMin'] = df['matchup_ptsPerMin'] - df['off_player_ptsPerMin']
	return df

def team_point_impact(df, matchup_min = 'matchup_min', matchup_team_pts = 'matchup_team_pts', off_team_ptsPerGame = 'avg_team_pts'):
	df['matchup_teamPtsPerMin'] = df[matchup_team_pts] / df[matchup_min]
	df['off_team_ptsPerMin'] = df[off_team_ptsPerGame] / 48.0
	df['playerImpact_teamPtsPerMin'] = df['matchup_teamPtsPerMin'] - df['off_team_ptsPerMin']
	return df

###									  ###
###									  ###
###        Efficiency Metrics         ###
###									  ###
###									  ###

def efg_impact(df, matchup_efg = 'matchup_efg', off_player_efg = 'off_player_efg'):
	df['playerImpact_EFG'] = df[matchup_efg] - df[off_player_efg]
	return df

def ts_impact(df, matchup_ts = 'matchup_ts', off_player_ts = 'off_player_ts'):
	df['playerImpact_EFG'] = df[matchup_ts] - df[off_player_ts]
	return df


###									  ###
###									  ###
###           Implementation          ###
###									  ###
###									  ###

grouped_player_impact_data = player_point_impact(grouped_player_data)
grouped_player_impact_data = team_point_impact(grouped_player_impact_data, off_team_ptsPerGame = 'avg_team_pts')

grouped_player_season_impact_data = player_point_impact(grouped_player_season_data)
grouped_player_season_impact_data = team_point_impact(grouped_player_impact_data)

grouped_player_impact_data = efg_impact(grouped_player_impact_data)
grouped_player_season_impact_data = efg_impact(grouped_player_season_impact_data)

grouped_player_impact_data = ts_impact(grouped_player_impact_data)
grouped_player_season_impact_data = ts_impact(grouped_player_season_impact_data)


###									  ###
###									  ###
###               Output              ###
###									  ###
###									  ###

grouped_player_impact_data.to_parquet('../Final Raw Data Files//grouped_player_impact_data.parquet')
grouped_player_season_impact_data.to_parquet('../Final Raw Data Files//grouped_player_season_impact_data.parquet')





